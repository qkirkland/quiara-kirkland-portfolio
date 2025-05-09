# Secure File Transfer Utility

A Python-based tool for securely transferring files over encrypted channels.

## Features
- Send and receive files securely
- Uses SSL/TLS for encrypted communication

## Setup
1. Install Python 3.7+
2. Install dependencies: `pip install -r requirements.txt`
3. Run sender: `python secure_file_transfer.py send <file> <host> <port>`
4. Run receiver: `python secure_file_transfer.py receive <port>`

## Usage
Ensure both sender and receiver have network connectivity and SSL certificates. 