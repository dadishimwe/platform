"""
Support-related schemas for the Starlink Platform API.
"""
from marshmallow import fields
from src.models import ma
from src.models.support import Ticket, TicketComment, KbCategory, KbArticle, ChatSession, ChatMessage

class TicketSchema(ma.SQLAlchemySchema):
    """Ticket schema."""
    class Meta:
        model = Ticket
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    organization_id = fields.String(required=True)
    user_id = fields.String(required=True)
    subject = fields.String(required=True)
    description = fields.String(required=True)
    status = fields.String()
    priority = fields.String()
    assigned_to = fields.String()
    closed_at = fields.DateTime()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class TicketCommentSchema(ma.SQLAlchemySchema):
    """Ticket Comment schema."""
    class Meta:
        model = TicketComment
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    ticket_id = fields.String(required=True)
    user_id = fields.String(required=True)
    comment = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class KbCategorySchema(ma.SQLAlchemySchema):
    """Knowledge Base Category schema."""
    class Meta:
        model = KbCategory
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    parent_id = fields.String()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class KbArticleSchema(ma.SQLAlchemySchema):
    """Knowledge Base Article schema."""
    class Meta:
        model = KbArticle
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    category_id = fields.String(required=True)
    title = fields.String(required=True)
    content = fields.String(required=True)
    author_id = fields.String(required=True)
    published_at = fields.DateTime()
    is_published = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ChatSessionSchema(ma.SQLAlchemySchema):
    """Chat Session schema."""
    class Meta:
        model = ChatSession
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    user_id = fields.String(required=True)
    agent_id = fields.String()
    status = fields.String()
    ended_at = fields.DateTime()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ChatMessageSchema(ma.SQLAlchemySchema):
    """Chat Message schema."""
    class Meta:
        model = ChatMessage
        load_instance = True
    
    id = ma.auto_field(dump_only=True)
    session_id = fields.String(required=True)
    sender_id = fields.String(required=True)
    message = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)


# Initialize schemas
ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)
ticket_comment_schema = TicketCommentSchema()
ticket_comments_schema = TicketCommentSchema(many=True)
kb_category_schema = KbCategorySchema()
kb_categories_schema = KbCategorySchema(many=True)
kb_article_schema = KbArticleSchema()
kb_articles_schema = KbArticleSchema(many=True)
chat_session_schema = ChatSessionSchema()
chat_sessions_schema = ChatSessionSchema(many=True)
chat_message_schema = ChatMessageSchema()
chat_messages_schema = ChatMessageSchema(many=True)

