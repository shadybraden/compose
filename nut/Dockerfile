# Use an appropriate base image
FROM alpine:latest

ENV TZ="America/New_York"

# Copy the shell script into the image
COPY nut.sh /nut.sh

# Make the script executable
RUN chmod +x /nut.sh

# Specify the command to run the script
CMD ["/nut.sh"]