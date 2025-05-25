"""
Utilitare pentru integrarea cu Gemini AI
"""
import google.generativeai as genai
from app.config import GEMINI_API_KEY
import logging
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class GeminiClient:
    _instance: Optional['GeminiClient'] = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeminiClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the Gemini client"""
        try:
            logger.debug("Initializing Gemini client...")
            genai.configure(api_key=GEMINI_API_KEY)
            self._model = genai.GenerativeModel('models/gemini-1.5-flash')
            logger.debug("Gemini client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Gemini client: {str(e)}")
            self._model = None
    
    def get_model(self):
        """Get the Gemini model instance"""
        if self._model is None:
            self._initialize()
        return self._model

async def get_gemini_response(prompt: str) -> str:
    """
    Obține un răspuns de la Gemini AI pentru un prompt dat
    
    Args:
        prompt (str): Prompt-ul utilizatorului
        
    Returns:
        str: Răspunsul de la Gemini
    """
    try:
        # Get model instance
        model = GeminiClient().get_model()
        if model is None:
            return "Error: Could not initialize Gemini model"
        
        # Adaugă context pentru travel assistant
        context = """You are a helpful travel assistant. Provide concise, 
        informative responses about travel destinations, planning, and tips. 
        Keep responses under 200 words and focus on practical advice."""
        
        full_prompt = f"{context}\n\nUser: {prompt}\nAssistant:"
        logger.debug(f"Sending prompt to Gemini: {prompt[:50]}...")
        
        # Generează răspunsul
        response = model.generate_content(full_prompt)
        logger.debug("Received response from Gemini")
        
        return response.text
        
    except Exception as e:
        error_msg = f"Error in get_gemini_response: {str(e)}"
        logger.error(error_msg)
        return f"Îmi pare rău, am întâmpinat o eroare: {str(e)}" 