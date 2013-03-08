import logging
import logging.handlers

import boto.sns

class SNSHandler(logging.Handler):
    ''' Python logging handler which publishes to Amazon AWS Simple 
    Notification Service. '''
    def __init__(self, topic="sns_handler_debug", aws_key=None, secret_key=None):
        logging.Handler.__init__(self)
        if aws_key and secret_key:
            self.conn = boto.sns.SNSConnection(aws_key, secret_key)
        else:
            self.conn = boto.sns.SNSConnection()

        topics = self.conn.get_all_topics()
        topics = topics["ListTopicsResponse"]["ListTopicsResult"]["Topics"]
        topics = [t['TopicArn'] for t in topics]
        try: 
            self.topic = [t for t in topics if t.split(':')[5] == topic][0]
        except: 
            raise "Topic not found"
        if not self.topic:
            raise "Topic not found"
        self.topic_name = topic
    
    def emit(self, record): 
        self.conn.publish(self.topic, record.msg)

if False: 
    logger = logging.getLogger('myapp')
    logger.addHandler(SNSHandler())
    logger.error("AAAA")
    logger.info("BBBB")
