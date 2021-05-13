import json

def image(image_url, alt_text=''):
    if not image_url:
        return None

    return {"type": "image", "image_url": image_url, "alt_text": alt_text}

def markdown(text):
    return MarkDown(text)

class MarkDown:
    def __init__(self, text, emoji=True):
        if text:
            self.text = text.strip()
        self.emoji = emoji

def fields(*args):
    return Fields(*args)

class Fields: 
    def __init__(self, *args):
        self.fields = [arg for arg in args if arg]
                
def blocks(*args):
    return Blocks(*args)

class Blocks: 
    def __init__(self, *args):
        self.blocks = [arg for arg in args if arg]
            
def section(*args):
    return Section(*args)

class Section:
    def __init__(self, *args):
        self.text = None
        self.fields = []
        for arg in args:
            if isinstance(arg, str) or isinstance(arg, PlainText) or isinstance(arg, MarkDown):
                self.text = arg
            elif isinstance(arg, Fields):
                self.fields = arg
            else:
                raise Exception("Type not supported for section")

def message(*args):
    return Message(*args)

def actions(*args):
    return {"type": "actions", "elements": [arg for arg in args if arg]}

def header(text):
    return Header(text)

class Header:
    def __init__(self, text):
        self.text = text
        
def plain_text(text, emoji=True):
    return PlainText(text, emoji)

class PlainText:
    def __init__(self, text, emoji):
        self.text = text.strip()
        self.emoji = emoji

class Message:
    def __init__(self, *args):
        self.text = None
        self.blocks = []
        
        for arg in args:
            if isinstance(arg, str):
                self.text = arg
            elif isinstance(arg, Blocks):
                self.blocks = arg
            else:
                raise Exception("Type not supported for message")

        pass
    
class Button:
    def __init__(self, text, value, action, action_id):
        self.text = text
        self.value = value
        self.action = action
        self.action_id = action_id
        pass
    
def button(text, value, action, action_id):
    return Button(text=text, value=value, action=action, action_id=action_id)

class BlockKitEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Button):
            return {"type": "button", "text": obj.text, "value": obj.value, "action_id": obj.action_id}
        if isinstance(obj, Fields):
            return obj.fields
        if isinstance(obj, Blocks):
            return obj.blocks
        if isinstance(obj, PlainText):
            return {"type": "plain_text", "text": obj.text, "emoji": obj.emoji}
        if isinstance(obj, MarkDown):
            return {"type": "mrkdwn", "text": obj.text.strip()}
        if isinstance(obj, Header):
            return {
                "type": "header",
                "text": obj.text,
            }
        if isinstance(obj, Message):
            v = {}
            if obj.text:
                v['text'] = obj.text
            if obj.blocks:
                v['blocks'] = obj.blocks
            return v
        if isinstance(obj, Section):
            v = {
                'type': 'section',
            }            
            if obj.text:
                v['text'] = obj.text
            if obj.fields:
                v['fields'] = obj.fields
            return v
            
        return json.JSONEncoder.default(self, obj)
    
