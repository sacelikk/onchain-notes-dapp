// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SecureNotes {
    struct Note {
        uint256 id;
        string title;
        string content;
        uint256 timestamp;
    }

    mapping(address => Note[]) private userNotes;

    event NoteAdded(address indexed user, uint256 id, string title);

    function addNote(string calldata _title, string calldata _content) external {
        uint256 noteId = userNotes[msg.sender].length;
        userNotes[msg.sender].push(Note({
            id: noteId,
            title: _title,
            content: _content,
            timestamp: block.timestamp
        }));
        emit NoteAdded(msg.sender, noteId, _title);
    }

    function getMyNotes() external view returns (Note[] memory) {
        return userNotes[msg.sender];
    }
}
