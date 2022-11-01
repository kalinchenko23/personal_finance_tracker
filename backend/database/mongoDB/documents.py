from datetime import datetime

import mongoengine
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, StringField, DateTimeField, FloatField, \
    ReferenceField, DynamicField

class Users(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    first_name = StringField(required=True, unique=True)
    last_name = StringField(required=True, unique=True)
    meta = {
        'indexes': ['$username']}

class Tokens(Document):
    user_id=ReferenceField('Users',reverse_delete_rule=mongoengine.NULLIFY)
    name= StringField()
    token= StringField(required=True)

class Accounts(Document):
    id = StringField(primary_key=True)
    name = StringField()
    balance = FloatField(required=True)
    subtype = StringField(required=True)


class Expenses_additional_info(EmbeddedDocument):
    category = StringField()
    merchant_name = StringField()
    meta = {
        'strict': False,
        'indexes': ['$merchant_name']
    }


class Expenses(Document):
    transaction_id = StringField(primary_key=True)
    created_date = StringField(required=True)
    amount = FloatField(required=True)
    account_id = ReferenceField('Accounts',reverse_delete_rule=mongoengine.NULLIFY)
    additional_info = EmbeddedDocumentField(Expenses_additional_info)
    meta = {
        'strict': False,
        'indexes': [
            'created_date'  # single-field index
             ],
        'ordering': ['-created_date']
    }
