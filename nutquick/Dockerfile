# Use an appropriate base image
FROM alpine:latest

ENV TZ="America/New_York"

# Copy the shell script into the image
COPY quicknut.sh /quicknut.sh

# Make the script executable
RUN chmod +x /quicknut.sh

# Specify the command to run the script
CMD ["/quicknut.sh"]