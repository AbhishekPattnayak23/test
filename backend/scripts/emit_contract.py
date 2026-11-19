#!/usr/bin/env python3
"""
API Contract Emitter for CV Villas Knowledge Assistant.
Generates API contract skeleton in .agent/contracts/api_contract.json
based on LLD specifications.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def generate_api_contract() -> Dict[str, Any]:
    """
    Generate API contract skeleton based on LLD specifications.
    
    Returns:
        Dictionary representing the API contract
    """
    
    # Base contract structure
    contract = {
        "application": "CV Villas Knowledge Assistant API",
        "version": "1.0.0",
        "description": "Backend API for CV Villas Knowledge Assistant - RAG-powered villa rental sales support",
        "generated_at": datetime.utcnow().isoformat(),
        "endpoints": {}
    }
    
    # Define all endpoints from LLD specifications
    endpoints = [
        # Authentication endpoints
        {
            "path": "/api/auth/login",
            "method": "POST",
            "summary": "Authenticate user and obtain JWT token",
            "description": "Authenticates user credentials and returns a JWT access token.",
            "tags": ["Authentication"],
            "request_body": {
                "email": "string",
                "password": "string"
            },
            "responses": {
                "200": {
                    "description": "Successful authentication",
                    "content": {
                        "access_token": "string",
                        "token_type": "string",
                        "expires_in": "integer",
                        "user": {
                            "id": "string",
                            "email": "string",
                            "role": "string",
                            "full_name": "string"
                        }
                    }
                },
                "401": {
                    "description": "Invalid credentials"
                }
            }
        },
        {
            "path": "/api/auth/logout",
            "method": "POST",
            "summary": "Invalidate user session",
            "description": "Invalidates the current user's JWT token.",
            "tags": ["Authentication"],
            "responses": {
                "200": {
                    "description": "Successfully logged out"
                },
                "401": {
                    "description": "Unauthorized"
                }
            }
        },
        {
            "path": "/api/auth/profile",
            "method": "GET",
            "summary": "Get current user profile",
            "description": "Retrieves the profile of the currently authenticated user.",
            "tags": ["Authentication"],
            "responses": {
                "200": {
                    "description": "User profile",
                    "content": {
                        "id": "string",
                        "email": "string",
                        "role": "string",
                        "full_name": "string",
                        "created_at": "datetime"
                    }
                },
                "401": {
                    "description": "Unauthorized"
                }
            }
        },
        
        # User management endpoints
        {
            "path": "/api/users",
            "method": "GET",
            "summary": "Get all users",
            "description": "Retrieves a list of all users (admin only).",
            "tags": ["Users"],
            "security": ["admin"],
            "responses": {
                "200": {
                    "description": "List of users",
                    "content": {
                        "users": [
                            {
                                "id": "string",
                                "email": "string",
                                "role": "string",
                                "full_name": "string",
                                "is_active": "boolean"
                            }
                        ],
                        "total": "integer"
                    }
                },
                "403": {
                    "description": "Forbidden - admin access required"
                }
            }
        },
        {
            "path": "/api/users/{id}",
            "method": "GET",
            "summary": "Get user by ID",
            "description": "Retrieves a specific user by their ID.",
            "tags": ["Users"],
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": "true",
                    "description": "User ID",
                    "schema": {
                        "type": "string"
                    }
                }
            ],
            "responses": {
                "200": {
                    "description": "User details"
                },
                "404": {
                    "description": "User not found"
                }
            }
        },
        {
            "path": "/api/users/{id}",
            "method": "PUT",
            "summary": "Update user",
            "description": "Updates a user's information.",
            "tags": ["Users"],
            "security": ["admin"],
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": "true",
                    "description": "User ID",
                    "schema": {
                        "type": "string"
                    }
                }
            ],
            "request_body": {
                "full_name": "string",
                "role": "string",
                "is_active": "boolean"
            },
            "responses": {
                "200": {
                    "description": "User updated successfully"
                },
                "403": {
                    "description": "Forbidden - insufficient permissions"
                },
                "404": {
                    "description": "User not found"
                }
            }
        },
        
        # Q&A endpoints
        {
            "path": "/api/answers/ask",
            "method": "POST",
            "summary": "Ask a question",
            "description": "Submit a question and receive an answer with citations from the RAG pipeline.",
            "tags": ["Q&A"],
            "security": ["agent", "expert", "admin"],
            "request_body": {
                "question": "string",
                "context": {
                    "villa_id": "string",
                    "user_id": "string"
                }
            },
            "responses": {
                "200": {
                    "description": "Answer generated successfully",
                    "content": {
                        "answer_id": "string",
                        "question": "string",
                        "answer_text": "string",
                        "confidence_score": "float",
                        "citations": [
                            {
                                "source_id": "string",
                                "excerpt": "string",
                                "relevance_score": "float",
                                "source_title": "string"
                            }
                        ],
                        "created_at": "datetime"
                    }
                },
                "400": {
                    "description": "Invalid question format"
                }
            }
        },
        {
            "path": "/api/answers",
            "method": "GET",
            "summary": "Get answer history",
            "description": "Retrieves the current user's answer history.",
            "tags": ["Q&A"],
            "security": ["agent", "expert", "admin"],
            "responses": {
                "200": {
                    "description": "List of answers",
                    "content": {
                        "answers": [
                            {
                                "id": "string",
                                "question": "string",
                                "answer_text": "string",
                                "confidence_score": "float",
                                "created_at": "datetime"
                            }
                        ],
                        "total": "integer"
                    }
                }
            }
        },
        {
            "path": "/api/answers/{id}",
            "method": "GET",
            "summary": "Get answer by ID",
            "description": "Retrieves a specific answer by its ID with citations.",
            "tags": ["Q&A"],
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": "true",
                    "description": "Answer ID",
                    "schema": {
                        "type": "string"
                    }
                }
            ],
            "responses": {
                "200": {
                    "description": "Answer details with citations"
                },
                "404": {
                    "description": "Answer not found"
                }
            }
        },
        {
            "path": "/api/answers/{id}/correct",
            "method": "POST",
            "summary": "Submit correction for answer",
            "description": "Experts can submit corrections for answers.",
            "tags": ["Q&A", "Corrections"],
            "security": ["expert", "admin"],
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": "true",
                    "description": "Answer ID",
                    "schema": {
                        "type": "string"
                    }
                }
            ],
            "request_body": {
                "correction_text": "string",
                "reason": "string"
            },
            "responses": {
                "200": {
                    "description": "Correction submitted successfully",
                    "content": {
                        "correction_id": "string",
                        "status": "string",
                        "message": "string"
                    }
                },
                "403": {
                    "description": "Forbidden - expert access required"
                },
                "404": {
                    "description": "Answer not found"
                }
            }
        },
        {
            "path": "/api/answers/{id}/escalate",
            "method": "POST",
            "summary": "Escalate low-confidence answer",
            "description": "Escalates a low-confidence answer for expert review.",
            "tags": ["Q&A", "Escalations"],
            "security": ["agent", "expert", "admin"],
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": "true",
                    "description": "Answer ID",
                    "schema": {
                        "type": "string"
                    }
                }
            ],
            "request_body": {
                "reason": "string"
            },
            "responses": {
                "200": {
                    "description": "Answer escalated successfully",
                    "content": {
                        "escalation_id": "string",
                        "status": "string",
                        "assigned_to": "string"
                    }
                },
                "400": {
                    "description": "Answer already escalated or cannot be escalated"
                }
            }
        },
        
        # Corrections management
        {
            "path": "/api/corrections",
            "method": "GET",
            "summary": "Get pending corrections",
            "description": "Retrieves all pending corrections for review.",
            "tags": ["Corrections"],
            "security": ["expert", "admin"],
            "responses": {
                "200": {
                    "description": "List of pending corrections",
                    "content": {
                        "corrections": [
                            {
                                "id": "string",
                                "answer_id": "string",
                                "question": "string",
                                "original_text": "string",
                                "correction_text": "string",
                                "submitted_by": "string",
                                "submitted_at": "datetime",
                                "status": "string"
                            }
                        ],
                        "total": "integer"
                    }
                }
            }
        },
        
        # Villa endpoints
        {
            "path": "/api/villas",
            "method": "GET",
            "summary": "Get all villas",
            "description": "Retrieves a list of all villas with filtering options.",
            "tags": ["Villas"],
            "security": ["guest", "agent", "expert", "admin"],
            "parameters": [
                {
                    "name": "location",
                    "in": "query",
                    "required": "false",
                    "description": "Filter by location",
                    "schema": {
                        "type": "string"
                    }
                },
                {
                    "name": "min_price",
                    "in": "query",
                    "required": "false",
                    "description": "Minimum price per week",
                    "schema": {
                        "type": "integer"
                    }
                },
                {
                    "name": "max_price",
                    "in": "query",
                    "required": "false",
                    "description": "Maximum price per week",
                    "schema": {
                        "type": "integer"
                    }
                },
                {
                    "name": "amenities",
                    "in": "query",
                    "required": "false",
                    "description": "Comma-separated list of amenities",
                    "schema": {
                        "type": "string"
                    }
                }
            ],
            "responses": {
                "200": {
                    "description": "List of villas",
                    "content": {
                        "villas": [
                            {
                                "id": "string",
                                "name": "string",
                                "location": "string",
                                "description": "string",
                                "amenities": ["string"],
                                "price_range_min": "integer",
                                "price_range_max": "integer",
                                "bedrooms": "integer",
                                "bathrooms": "integer",
                                "capacity": "integer"
                            }
                        ],
                        "total": "integer"
                    }
                }
            }
        },
        {
            "path": "/api/villas/{id}",
            "method": "GET",
            "summary": "Get villa by ID",
            "description": "Retrieves detailed information about a specific villa.",
            "tags": ["Villas"],
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": "true",
                    "description": "Villa ID",
                    "schema": {
                        "type": "string"
                    }
                }
            ],
            "responses": {
                "200": {
                    "description": "Villa details",
                    "content": {
                        "id": "string",
                        "name": "string",
                        "location": "string",
                        "description": "string",
                        "amenities": ["string"],
                        "price_range_min": "integer",
                        "price_range_max": "integer",
                        "bedrooms": "integer",
                        "bathrooms": "integer",
                        "capacity": "integer",
                        "images": ["string"],
                        "knowledge_sources": [
                            {
                                "id": "string",
                                "type": "string",
                                "title": "string",
                                "content": "string"
                            }
                        ]
                    }
                },
                "404": {
                    "description": "Villa not found"
                }
            }
        },
        
        # Knowledge sources endpoints
        {
            "path": "/api/knowledge-sources",
            "method": "GET",
            "summary": "Get all knowledge sources",
            "description": "Retrieves a list of all knowledge sources in the system.",
            "tags": ["Knowledge Sources"],
            "security": ["expert", "admin"],
            "responses": {
                "200": {
                    "description": "List of knowledge sources",
                    "content": {
                        "knowledge_sources": [
                            {
                                "id": "string",
                                "type": "string",
                                "title": "string",
                                "content": "string",
                                "source_uri": "string",
                                "ingested_at": "datetime"
                            }
                        ],
                        "total": "integer"
                    }
                }
            }
        },
        
        # Coverage gaps endpoints
        {
            "path": "/api/coverage-gaps",
            "method": "GET",
            "summary": "Get coverage gaps report",
            "description": "Retrieves report of identified knowledge coverage gaps.",
            "tags": ["Analytics"],
            "security": ["admin"],
            "responses": {
                "200": {
                    "description": "Coverage gaps report",
                    "content": {
                        "gaps": [
                            {
                                "id": "string",
                                "question": "string",
                                "confidence_score": "float",
                                "gap_type": "string",
                                "priority": "string",
                                "status": "string",
                                "created_at": "datetime"
                            }
                        ],
                        "total": "integer",
                        "summary": {
                            "open_gaps": "integer",
                            "high_priority": "integer",
                            "investigating": "integer"
                        }
                    }
                }
            }
        },
        
        # Admin endpoints
        {
            "path": "/api/admin/seed",
            "method": "POST",
            "summary": "Seed database",
            "description": "Populates the database with sample data for development.",
            "tags": ["Admin"],
            "security": ["admin"],
            "responses": {
                "200": {
                    "description": "Database seeded successfully",
                    "content": {
                        "message": "string",
                        "records_created": "integer"
                    }
                }
            }
        },
        {
            "path": "/api/admin/reset",
            "method": "POST",
            "summary": "Reset database",
            "description": "Resets the database (development only).",
            "tags": ["Admin"],
            "security": ["admin"],
            "responses": {
                "200": {
                    "description": "Database reset successfully"
                },
                "403": {
                    "description": "Forbidden - production environment"
                }
            }
        },
        {
            "path": "/api/admin/audit-logs",
            "method": "GET",
            "summary": "Get audit logs",
            "description": "Retrieves system audit logs.",
            "tags": ["Admin"],
            "security": ["admin"],
            "parameters": [
                {
                    "name": "limit",
                    "in": "query",
                    "required": "false",
                    "description": "Maximum number of logs to return",
                    "schema": {
                        "type": "integer",
                        "default": 100
                    }
                },
                {
                    "name": "offset",
                    "in": "query",
                    "required": "false",
                    "description": "Offset for pagination",
                    "schema": {
                        "type": "integer",
                        "default": 0
                    }
                }
            ],
            "responses": {
                "200": {
                    "description": "List of audit logs",
                    "content": {
                        "logs": [
                            {
                                "id": "string",
                                "user_id": "string",
                                "action": "string",
                                "entity_type": "string",
                                "entity_id": "string",
                                "timestamp": "datetime",
                                "metadata": "object"
                            }
                        ],
                        "total": "integer"
                    }
                }
            }
        },
        {
            "path": "/api/admin/config",
            "method": "GET",
            "summary": "Get system configuration",
            "description": "Retrieves current system configuration settings.",
            "tags": ["Admin"],
            "security": ["admin"],
            "responses": {
                "200": {
                    "description": "System configuration",
                    "content": {
                        "configurations": [
                            {
                                "key": "string",
                                "value": "any",
                                "value_type": "string",
                                "category": "string",
                                "description": "string"
                            }
                        ]
                    }
                }
            }
        }
    ]
    
    # Add endpoints to contract
    for endpoint in endpoints:
        # Create a unique key for the endpoint
        key = f"{endpoint['method']}:{endpoint['path']}"
        contract["endpoints"][key] = endpoint
    
    return contract


def write_contract_to_file(contract: Dict[str, Any], output_path: str) -> None:
    """
    Write API contract to JSON file.
    
    Args:
        contract: API contract dictionary
        output_path: Path to output JSON file
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write contract to JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(contract, f, indent=2, default=str)
    
    print(f"API contract written to {output_path}")
    print(f"Total endpoints: {len(contract['endpoints'])}")


def main():
    """Main function to generate and save API contract."""
    # Generate API contract
    print("Generating API contract skeleton...")
    contract = generate_api_contract()
    
    # Define output path
    output_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".agent",
        "contracts",
        "api_contract.json"
    )
    
    # Write contract to file
    write_contract_to_file(contract, output_path)
    
    # Also write to a backup location for reference
    backup_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "docs",
        "api_contract.json"
    )
    
    # Create docs directory if it doesn't exist
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(contract, f, indent=2, default=str)
    
    print(f"Backup contract written to {backup_path}")
    
    print("API contract generation completed successfully!")


if __name__ == "__main__":
    main()