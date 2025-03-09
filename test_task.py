from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
import asyncio
import os
from pydantic import SecretStr


api_key = os.getenv("DEEPSEEK_API_KEY")

# Configure the browser to connect to your Chrome instance
browser = Browser(
    config=BrowserConfig(
        # Specify the path to your Chrome executable
        # chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS path
        #"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        # chrome_instance_path='/usr/bin/google-chrome'
        headless=False
    )
)

# Create the agent with your configured browser
agent = Agent(
    task="go to weibo and search for current 微博热搜, save the result in a csv file including url, ask me for help if necessary",
    llm=ChatOpenAI(base_url='https://api.deepseek.com/v1', model='deepseek-reasoner', api_key=SecretStr(api_key)),
    browser=browser,
)

async def main():
    await agent.run()

    input('Press Enter to close the browser...')
    await browser.close()

if __name__ == '__main__':
    asyncio.run(main())

    # xvfb-run --server-args='-screen 0 1280x1024x24' python test_task.py