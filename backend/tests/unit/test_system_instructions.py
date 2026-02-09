"""
Unit tests for system instructions.

Tests that system instructions are properly defined and loaded.
"""

import pytest

from src.agents.system_instructions import (
    SYSTEM_INSTRUCTIONS,
    get_system_instructions
)


class TestSystemInstructions:
    """Tests for system instructions."""
    
    def test_instructions_not_empty(self):
        """Test that system instructions are not empty."""
        assert SYSTEM_INSTRUCTIONS
        assert len(SYSTEM_INSTRUCTIONS.strip()) > 0
    
    def test_instructions_contain_key_sections(self):
        """Test that instructions contain all required sections."""
        instructions = SYSTEM_INSTRUCTIONS.lower()
        
        # Check for key sections
        assert "capabilities" in instructions or "can help" in instructions
        assert "communication style" in instructions or "be friendly" in instructions
        assert "add task" in instructions or "create" in instructions
        assert "list task" in instructions or "show" in instructions
        assert "complete" in instructions or "mark" in instructions
        assert "delete" in instructions or "remove" in instructions
        assert "update" in instructions or "modify" in instructions
    
    def test_instructions_mention_tools(self):
        """Test that instructions mention using tools."""
        instructions = SYSTEM_INSTRUCTIONS.lower()
        assert "tool" in instructions or "use" in instructions
    
    def test_instructions_define_persona(self):
        """Test that instructions define a friendly persona."""
        instructions = SYSTEM_INSTRUCTIONS.lower()
        assert "friendly" in instructions or "helpful" in instructions
    
    def test_get_system_instructions_returns_string(self):
        """Test that get_system_instructions returns a string."""
        instructions = get_system_instructions()
        assert isinstance(instructions, str)
        assert len(instructions) > 100  # Should be substantial
    
    def test_get_system_instructions_matches_constant(self):
        """Test that function returns the same as constant."""
        assert get_system_instructions() == SYSTEM_INSTRUCTIONS
    
    def test_instructions_have_examples(self):
        """Test that instructions include example interactions."""
        instructions = SYSTEM_INSTRUCTIONS.lower()
        assert "example" in instructions or "user:" in instructions
    
    def test_instructions_mention_confirmation(self):
        """Test that instructions emphasize confirmations."""
        instructions = SYSTEM_INSTRUCTIONS.lower()
        assert "confirm" in instructions or "done" in instructions
