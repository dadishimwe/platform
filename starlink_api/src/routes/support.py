"""
Support routes for the Starlink Platform API.
"""
from datetime import datetime
from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from src.models import db
from src.models.support import Ticket, TicketComment, KbCategory, KbArticle, ChatSession, ChatMessage
from src.models.user import User
from src.models.organization import Organization
from src.schemas.support import (
    ticket_schema, tickets_schema, ticket_comment_schema, ticket_comments_schema,
    kb_category_schema, kb_categories_schema, kb_article_schema, kb_articles_schema,
    chat_session_schema, chat_sessions_schema, chat_message_schema, chat_messages_schema
)
from src.utils.responses import success_response, error_response, pagination_response
from src.utils.error_handlers import NotFoundError, ValidationError as APIValidationError
from src.utils.auth import permission_required

support_bp = Blueprint('support', __name__)

# Ticket routes
@support_bp.route('/tickets', methods=['GET'])
@jwt_required()
@permission_required('support', 'read')
def get_tickets():
    """Get all tickets."""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        organization_id = request.args.get('organization_id')
        user_id = request.args.get('user_id')
        status = request.args.get('status')
        priority = request.args.get('priority')
        
        # Build query
        query = Ticket.query
        
        # Apply filters
        if organization_id:
            query = query.filter_by(organization_id=organization_id)
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        if priority:
            query = query.filter_by(priority=priority)
        
        # Query tickets with pagination
        pagination = query.order_by(Ticket.created_at.desc()).paginate(page=page, per_page=per_page)
        
        # Return paginated tickets
        return pagination_response(
            tickets_schema.dump(pagination.items),
            page,
            per_page,
            pagination.total
        )
    
    except Exception as e:
        current_app.logger.error(f"Get tickets error: {str(e)}")
        return error_response('An error occurred while getting tickets', status_code=500)


@support_bp.route('/tickets/<ticket_id>', methods=['GET'])
@jwt_required()
@permission_required('support', 'read')
def get_ticket(ticket_id):
    """Get ticket by ID."""
    try:
        # Find ticket
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            raise NotFoundError('Ticket not found')
        
        # Return ticket
        return success_response(ticket_schema.dump(ticket))
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Get ticket error: {str(e)}")
        return error_response('An error occurred while getting ticket', status_code=500)


@support_bp.route('/tickets', methods=['POST'])
@jwt_required()
@permission_required('support', 'create')
def create_ticket():
    """Create a new ticket."""
    try:
        # Get current user ID from token
        current_user_id = get_jwt_identity()
        
        # Validate request data
        data = ticket_schema.load(request.json)
        
        # Check if organization exists
        organization = Organization.query.get(data.organization_id)
        if not organization:
            raise NotFoundError('Organization not found')
        
        # Set user ID to current user if not provided
        if not data.user_id:
            data.user_id = current_user_id
        
        # Save ticket to database
        db.session.add(data)
        db.session.commit()
        
        # Return created ticket
        return success_response(ticket_schema.dump(data), 'Ticket created successfully', status_code=201)
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Create ticket error: {str(e)}")
        return error_response('An error occurred while creating ticket', status_code=500)


@support_bp.route('/tickets/<ticket_id>', methods=['PUT'])
@jwt_required()
@permission_required('support', 'update')
def update_ticket(ticket_id):
    """Update ticket by ID."""
    try:
        # Find ticket
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            raise NotFoundError('Ticket not found')
        
        # Validate request data
        data = ticket_schema.load(request.json, instance=ticket, partial=True)
        
        # Save changes to database
        db.session.commit()
        
        # Return updated ticket
        return success_response(ticket_schema.dump(data), 'Ticket updated successfully')
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Update ticket error: {str(e)}")
        return error_response('An error occurred while updating ticket', status_code=500)


@support_bp.route('/tickets/<ticket_id>/comments', methods=['GET'])
@jwt_required()
@permission_required('support', 'read')
def get_ticket_comments(ticket_id):
    """Get ticket comments."""
    try:
        # Find ticket
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            raise NotFoundError('Ticket not found')
        
        # Get ticket comments
        comments = TicketComment.query.filter_by(ticket_id=ticket_id).order_by(TicketComment.created_at).all()
        
        # Return ticket comments
        return success_response(ticket_comments_schema.dump(comments))
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Get ticket comments error: {str(e)}")
        return error_response('An error occurred while getting ticket comments', status_code=500)


@support_bp.route('/tickets/<ticket_id>/comments', methods=['POST'])
@jwt_required()
@permission_required('support', 'update')
def add_ticket_comment(ticket_id):
    """Add comment to ticket."""
    try:
        # Get current user ID from token
        current_user_id = get_jwt_identity()
        
        # Find ticket
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            raise NotFoundError('Ticket not found')
        
        # Validate request data
        data = ticket_comment_schema.load(request.json)
        
        # Set ticket ID and user ID
        data.ticket_id = ticket_id
        data.user_id = current_user_id
        
        # Save to database
        db.session.add(data)
        db.session.commit()
        
        # Return success message
        return success_response(
            ticket_comment_schema.dump(data),
            'Comment added successfully',
            status_code=201
        )
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Add ticket comment error: {str(e)}")
        return error_response('An error occurred while adding comment', status_code=500)


# Knowledge Base routes
@support_bp.route('/kb/categories', methods=['GET'])
@jwt_required()
def get_kb_categories():
    """Get all knowledge base categories."""
    try:
        # Get query parameters
        parent_id = request.args.get('parent_id')
        
        # Build query
        query = KbCategory.query
        
        # Apply filters
        if parent_id:
            query = query.filter_by(parent_id=parent_id)
        else:
            # Get top-level categories (no parent)
            query = query.filter_by(parent_id=None)
        
        # Get categories
        categories = query.all()
        
        # Return categories
        return success_response(kb_categories_schema.dump(categories))
    
    except Exception as e:
        current_app.logger.error(f"Get KB categories error: {str(e)}")
        return error_response('An error occurred while getting knowledge base categories', status_code=500)


@support_bp.route('/kb/categories/<category_id>', methods=['GET'])
@jwt_required()
def get_kb_category(category_id):
    """Get knowledge base category by ID."""
    try:
        # Find category
        category = KbCategory.query.get(category_id)
        if not category:
            raise NotFoundError('Category not found')
        
        # Return category
        return success_response(kb_category_schema.dump(category))
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Get KB category error: {str(e)}")
        return error_response('An error occurred while getting knowledge base category', status_code=500)


@support_bp.route('/kb/categories', methods=['POST'])
@jwt_required()
@permission_required('support', 'create')
def create_kb_category():
    """Create a new knowledge base category."""
    try:
        # Validate request data
        data = kb_category_schema.load(request.json)
        
        # Check if parent category exists if provided
        if data.parent_id:
            parent = KbCategory.query.get(data.parent_id)
            if not parent:
                raise NotFoundError('Parent category not found')
        
        # Save category to database
        db.session.add(data)
        db.session.commit()
        
        # Return created category
        return success_response(kb_category_schema.dump(data), 'Category created successfully', status_code=201)
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Create KB category error: {str(e)}")
        return error_response('An error occurred while creating knowledge base category', status_code=500)


@support_bp.route('/kb/articles', methods=['GET'])
@jwt_required()
def get_kb_articles():
    """Get knowledge base articles."""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        category_id = request.args.get('category_id')
        is_published = request.args.get('is_published', type=bool)
        
        # Build query
        query = KbArticle.query
        
        # Apply filters
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if is_published is not None:
            query = query.filter_by(is_published=is_published)
        
        # Query articles with pagination
        pagination = query.order_by(KbArticle.created_at.desc()).paginate(page=page, per_page=per_page)
        
        # Return paginated articles
        return pagination_response(
            kb_articles_schema.dump(pagination.items),
            page,
            per_page,
            pagination.total
        )
    
    except Exception as e:
        current_app.logger.error(f"Get KB articles error: {str(e)}")
        return error_response('An error occurred while getting knowledge base articles', status_code=500)


@support_bp.route('/kb/articles/<article_id>', methods=['GET'])
@jwt_required()
def get_kb_article(article_id):
    """Get knowledge base article by ID."""
    try:
        # Find article
        article = KbArticle.query.get(article_id)
        if not article:
            raise NotFoundError('Article not found')
        
        # Return article
        return success_response(kb_article_schema.dump(article))
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Get KB article error: {str(e)}")
        return error_response('An error occurred while getting knowledge base article', status_code=500)


@support_bp.route('/kb/articles', methods=['POST'])
@jwt_required()
@permission_required('support', 'create')
def create_kb_article():
    """Create a new knowledge base article."""
    try:
        # Get current user ID from token
        current_user_id = get_jwt_identity()
        
        # Validate request data
        data = kb_article_schema.load(request.json)
        
        # Check if category exists
        category = KbCategory.query.get(data.category_id)
        if not category:
            raise NotFoundError('Category not found')
        
        # Set author ID to current user if not provided
        if not data.author_id:
            data.author_id = current_user_id
        
        # Save article to database
        db.session.add(data)
        db.session.commit()
        
        # Return created article
        return success_response(kb_article_schema.dump(data), 'Article created successfully', status_code=201)
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Create KB article error: {str(e)}")
        return error_response('An error occurred while creating knowledge base article', status_code=500)


@support_bp.route('/kb/articles/<article_id>', methods=['PUT'])
@jwt_required()
@permission_required('support', 'update')
def update_kb_article(article_id):
    """Update knowledge base article by ID."""
    try:
        # Find article
        article = KbArticle.query.get(article_id)
        if not article:
            raise NotFoundError('Article not found')
        
        # Validate request data
        data = kb_article_schema.load(request.json, instance=article, partial=True)
        
        # Check if category exists if provided
        if 'category_id' in request.json:
            category = KbCategory.query.get(data.category_id)
            if not category:
                raise NotFoundError('Category not found')
        
        # Save changes to database
        db.session.commit()
        
        # Return updated article
        return success_response(kb_article_schema.dump(data), 'Article updated successfully')
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Update KB article error: {str(e)}")
        return error_response('An error occurred while updating knowledge base article', status_code=500)


# Chat routes
@support_bp.route('/chat/sessions', methods=['GET'])
@jwt_required()
@permission_required('support', 'read')
def get_chat_sessions():
    """Get chat sessions."""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        user_id = request.args.get('user_id')
        agent_id = request.args.get('agent_id')
        status = request.args.get('status')
        
        # Build query
        query = ChatSession.query
        
        # Apply filters
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        if agent_id:
            query = query.filter_by(agent_id=agent_id)
        
        if status:
            query = query.filter_by(status=status)
        
        # Query chat sessions with pagination
        pagination = query.order_by(ChatSession.created_at.desc()).paginate(page=page, per_page=per_page)
        
        # Return paginated chat sessions
        return pagination_response(
            chat_sessions_schema.dump(pagination.items),
            page,
            per_page,
            pagination.total
        )
    
    except Exception as e:
        current_app.logger.error(f"Get chat sessions error: {str(e)}")
        return error_response('An error occurred while getting chat sessions', status_code=500)


@support_bp.route('/chat/sessions/<session_id>', methods=['GET'])
@jwt_required()
@permission_required('support', 'read')
def get_chat_session(session_id):
    """Get chat session by ID."""
    try:
        # Find chat session
        session = ChatSession.query.get(session_id)
        if not session:
            raise NotFoundError('Chat session not found')
        
        # Return chat session
        return success_response(chat_session_schema.dump(session))
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Get chat session error: {str(e)}")
        return error_response('An error occurred while getting chat session', status_code=500)


@support_bp.route('/chat/sessions', methods=['POST'])
@jwt_required()
def create_chat_session():
    """Create a new chat session."""
    try:
        # Get current user ID from token
        current_user_id = get_jwt_identity()
        
        # Validate request data
        data = chat_session_schema.load(request.json)
        
        # Set user ID to current user if not provided
        if not data.user_id:
            data.user_id = current_user_id
        
        # Save chat session to database
        db.session.add(data)
        db.session.commit()
        
        # Return created chat session
        return success_response(chat_session_schema.dump(data), 'Chat session created successfully', status_code=201)
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except Exception as e:
        current_app.logger.error(f"Create chat session error: {str(e)}")
        return error_response('An error occurred while creating chat session', status_code=500)


@support_bp.route('/chat/sessions/<session_id>/messages', methods=['GET'])
@jwt_required()
@permission_required('support', 'read')
def get_chat_messages(session_id):
    """Get chat messages for a session."""
    try:
        # Find chat session
        session = ChatSession.query.get(session_id)
        if not session:
            raise NotFoundError('Chat session not found')
        
        # Get chat messages
        messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.created_at).all()
        
        # Return chat messages
        return success_response(chat_messages_schema.dump(messages))
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Get chat messages error: {str(e)}")
        return error_response('An error occurred while getting chat messages', status_code=500)


@support_bp.route('/chat/sessions/<session_id>/messages', methods=['POST'])
@jwt_required()
def send_chat_message(session_id):
    """Send a chat message."""
    try:
        # Get current user ID from token
        current_user_id = get_jwt_identity()
        
        # Find chat session
        session = ChatSession.query.get(session_id)
        if not session:
            raise NotFoundError('Chat session not found')
        
        # Check if session is open
        if session.status != 'open':
            raise APIValidationError('Chat session is not open')
        
        # Validate request data
        data = chat_message_schema.load(request.json)
        
        # Set session ID and sender ID
        data.session_id = session_id
        data.sender_id = current_user_id
        
        # Save to database
        db.session.add(data)
        db.session.commit()
        
        # Return success message
        return success_response(
            chat_message_schema.dump(data),
            'Message sent successfully',
            status_code=201
        )
    
    except ValidationError as e:
        return error_response('Validation error', errors=e.messages)
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except APIValidationError as e:
        return error_response(str(e))
    
    except Exception as e:
        current_app.logger.error(f"Send chat message error: {str(e)}")
        return error_response('An error occurred while sending chat message', status_code=500)


@support_bp.route('/chat/sessions/<session_id>/close', methods=['POST'])
@jwt_required()
def close_chat_session(session_id):
    """Close a chat session."""
    try:
        # Find chat session
        session = ChatSession.query.get(session_id)
        if not session:
            raise NotFoundError('Chat session not found')
        
        # Check if session is already closed
        if session.status == 'closed':
            return success_response(message='Chat session is already closed')
        
        # Close session
        session.status = 'closed'
        session.ended_at = datetime.utcnow()
        db.session.commit()
        
        # Return success message
        return success_response(message='Chat session closed successfully')
    
    except NotFoundError as e:
        return error_response(str(e), status_code=404)
    
    except Exception as e:
        current_app.logger.error(f"Close chat session error: {str(e)}")
        return error_response('An error occurred while closing chat session', status_code=500)

