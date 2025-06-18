# Use an appropriate base image
FROM alpine:latest

ENV TZ="America/New_York"

# Copy the shell script into the image
COPY ups_monitor.sh /ups_monitor.sh

# Make the script executable
RUN chmod +x /ups_monitor.sh

# Specify the command to run the script
CMD ["/ups_monitor.sh"]