from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    firstname = fields.Str(required=True, validate=validate.Length(min=1))
    lastname = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))


class TaskSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1))
    body = fields.Str()
    completed = fields.Bool()
    due_date = fields.Str()


class ResetPassword(Schema):
    email = fields.Email(required=True)


class UpdatePassword(Schema):
    password = fields.Str(required=True, validate=validate.Length(min=8))
    token = fields.Str(required=True)