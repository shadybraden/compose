#!/bin/bash

# Variables for source and destination
SOURCE="/data/restic/" # put the whole restic folder. each folder inside will be there
DESTINATION="awss3:bucket/folder"

# Docker container name (replace with your container name if different)
CONTAINER_NAME="rclone"

# ntfy configuration - replace with your ntfy topic and URL
NTFY_TOPIC="backups"
NTFY_URL="https://ntfy.example.com/$NTFY_TOPIC"
NTFY_TITLE="server rclone-s3 starting..."
NTFY_MESSAGE=""
PRIORITY="min"
TAG="house"
# Read AWS credentials from keys.conf
source <(grep -E 'access_key_id|secret_access_key' /home/user/rclone_restic/keys.conf | sed 's/ *=/=/')

# Export the AWS credentials as environment variables
export AWS_ACCESS_KEY_ID="$access_key_id"
export AWS_SECRET_ACCESS_KEY="$secret_access_key"

echo "pre checking aws"
# Run the AWS S3 command and store the last line of the output in the TOTAL_S3_SIZE variable
PRE_TOTAL_S3_SIZE=$(aws s3 ls --summarize --human-readable --recursive s3://bucket/ | tail -n 1)
echo "$PRE_TOTAL_S3_SIZE"

echo "upload to aws"
# Run the rclone copy command inside the Docker container
RCLONE_OUTPUT=$(docker exec "$CONTAINER_NAME" rclone sync "$SOURCE" "$DESTINATION" --progress 2>&1)
RCLONE_TRIMMED_OUTPUT=${RCLONE_OUTPUT: -200}
echo "$RCLONE_TRIMMED_OUTPUT"

echo "post checking aws"
POST_TOTAL_S3_SIZE=$(aws s3 ls --summarize --human-readable --recursive s3://bucket/ | tail -n 1)
echo "$POST_TOTAL_S3_SIZE"

if [ $? -eq 0 ]; then
    NTFY_MESSAGE="$RCLONE_TRIMMED_OUTPUT"
    NTFY_TITLE="server rclone-s3 success"
else
    NTFY_MESSAGE="Error: Failed to copy data to S3.\n\nOutput:\n$RCLONE_OUTPUT"
    NTFY_TITLE="RCLONE-S3 FAILED"
    TAG="warning"
    PRIORITY="high"
fi

#check local size
RCLONE_S3_SIZE=$(docker exec "$CONTAINER_NAME" rclone size "$SOURCE" --json | jq '.bytes' | awk '{print "Size of restic folder " $1/1024/1024/1024 " GB"}')

# ---
# message here:
ACTUALLY_SEND="$PRE_TOTAL_S3_SIZE"$'\n'"$RCLONE_S3_SIZE"$'\n'"$POST_TOTAL_S3_SIZE"$'\n'$'\n'"$NTFY_MESSAGE"

# Send the notification via ntfy
#curl -X POST -d "$RCLONE_S3_SIZE"$'\n'"$NTFY_MESSAGE" "$NTFY_URL" \
curl -X POST -d "$ACTUALLY_SEND" "$NTFY_URL" \
  -H "Title: $NTFY_TITLE" \
  -H "Tags: $TAG" \
  -H "Priority: $PRIORITY"
