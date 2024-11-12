FinAI - Personal Finance Assistant with Local LLM
FinAI is a privacy-first personal finance management application that helps users gain insights into their spending patterns and achieve financial goals. Powered by a local LLaMA 3.2 model, FinAI ensures that user data remains private, as no data is shared externally. The app allows users to analyze expenses, track financial goals, and interact with an AI chatbot for personalized financial advice.

Features
Data Analysis and Visualization: Interactive charts for income, expenses, category breakdowns, and monthly/annual summaries.
Financial Goals Tracking: Set, track, and manage financial goals with progress visualizations.
Secure AI Chatbot: Get personalized financial suggestions through a locally hosted LLM with Whisper for voice-to-text capabilities.
Customizable Categories: Define expense categories to tailor the analysis to your specific needs.
Real-time Expense Tracking: Add or update expenses manually and categorize them easily.

Tech Stack
Frontend: Streamlit
Backend: Appwrite for data storage, Pandas for data processing
AI Models: Meta’s LLaMA 3.2 for chatbot, OpenAI’s Whisper for voice recognition
Visualization: Plotly for data visualization

Installation
Clone this repository:
bash
git clone https://github.com/yourusername/finai.git
cd finai
Install the required dependencies:

bash
pip install -r requirements.txt
Run the Streamlit app:

bash
streamlit run app.py


Usage
Upload a CSV file with transaction data or enter expenses manually.
View categorized transactions, financial goals, and interactive charts.
Use the AI chatbot to ask financial questions or set financial goals. You can type or use voice commands.
Check your progress on financial goals and receive tailored suggestions from the chatbot.

Project Structure
app.py: Main application file to start the Streamlit app.
layout.py: Layout structure for the dashboard and UI components.
chart_ui.py: Handles the rendering of charts for data visualization.
llm_chat.py: Manages interactions with the LLaMA model and Whisper for the AI chatbot.
goal_manager.py: Manages user-defined financial goals.
metrics.py: Defines functions for calculating financial metrics.
charts.py: Contains functions for creating various data visualizations.

Data Privacy
FinAI is designed with a focus on user data privacy. All data processing and AI interactions occur locally, ensuring that no personal data is shared or stored externally.

Future Scope
Add advanced financial planning tools, like budget variance analysis and automatic savings suggestions.
Integrate predictive analysis for long-term financial forecasting.
Expand voice interaction capabilities and add more interactive dashboard features.

Contributing
Contributions are welcome! Please fork this repository, make changes, and submit a pull request.

