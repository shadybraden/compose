# Use an appropriate base image
FROM alpine:latest

ENV TZ="America/New_York"

WORKDIR /app

COPY . /app

# Copy the shell script into the image
#COPY nut.sh /app/nut.sh

# Make the script executable
RUN chmod +x /app/nut.sh

# Specify the command to run the script
CMD ["/app/nut.sh"]