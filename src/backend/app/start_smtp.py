from aiosmtpd.controller import Controller

class DebuggingHandler:
    async def handle_DATA(self, server, session, envelope):
        print("Message received:")
        print(envelope.content.decode('utf8', errors='replace'))
        return '250 OK'

if __name__ == '__main__':
    controller = Controller(DebuggingHandler(), hostname='localhost', port=1025)
    print("Starting SMTP Debugging server at localhost:1025...")
    controller.start()
