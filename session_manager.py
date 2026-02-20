from datetime import datetime, timedelta

class SessionManager:
    """
    Manages user sessions and conversation context.
    """

    SESSION_TIMEOUT = timedelta(minutes=30)  # 30-minute inactivity

    def __init__(self):
        # In-memory session storage: {session_id: {context, last_updated}}
        self.sessions = {}

    def get_or_create(self, session_id: str) -> dict:
        """
        Retrieve an existing session or create a new one.
        Returns session dictionary with 'context' and 'last_updated'.
        """
        if session_id in self.sessions:
            session = self.sessions[session_id]
            if self.is_expired(session_id):
                self.sessions.pop(session_id)
            else:
                return session

        # Create new session
        session = {"context": {}, "last_updated": datetime.utcnow()}
        self.sessions[session_id] = session
        return session

    def update(self, session_id: str, context_update: dict):
        """
        Update session context and refresh last_updated timestamp.
        """
        session = self.get_or_create(session_id)
        session["context"].update(context_update)
        session["last_updated"] = datetime.utcnow()
        self.sessions[session_id] = session

    def is_expired(self, session_id: str) -> bool:
        """
        Check if session is expired based on last_updated timestamp.
        """
        session = self.sessions.get(session_id)
        if not session:
            return True
        return datetime.utcnow() - session["last_updated"] > self.SESSION_TIMEOUT

    def clear_expired_sessions(self):
        """
        Optional: Remove all expired sessions from memory.
        """
        expired_keys = [sid for sid in self.sessions if self.is_expired(sid)]
        for sid in expired_keys:
            self.sessions.pop(sid)
