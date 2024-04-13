# Import Gemini library
import google.generativeai as genai

from config import API_KEY

# Configure Gemini API with the imported key
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(model_name="gemini-pro")

import asyncio
from pyppeteer import launch

# Import not required for Gemini API


async def scrape_reviews(url):
    reviews = []

    browser = await launch({"headless": True, "args": ["--window-size=800,3200"]})

    page = await browser.newPage()
    await page.setViewport({"width": 800, "height": 3200})
    await page.goto(url)
    await page.waitForSelector(".jftiEf")

    elements = await page.querySelectorAll(".jftiEf")
    for element in elements:
        try:
            await page.waitForSelector(".w8nwRe")
            more_btn = await element.querySelector(".w8nwRe")
            await page.evaluate("button => button.click()", more_btn)
            await page.waitFor(5000)
        except:
            pass

        await page.waitForSelector(".MyEned")
        snippet = await element.querySelector(".MyEned")
        text = await page.evaluate("selected => selected.textContent", snippet)
        reviews.append(text)

    await browser.close()

    return reviews


def summarize(reviews, model):
    prompt = "I collected some reviews of a place I was considering visiting. \
                 Can you summarize the reviews for me? I want to generally know what people \
                 like and dislike as well as most selling items. The reviews are below and list them in order:\n"
    for review in reviews:
        prompt += "\n" + review

    # Generate content using Gemini model
    completion = model.generate_content(
        prompt,
        generation_config={"temperature": 0, "max_output_tokens": 3000},  # Optional parameters
    )

    return completion.text


# No need for palm.list_models() or model selection

url = input("Enter a url: ")

reviews = asyncio.get_event_loop().run_until_complete(scrape_reviews(url))

result = summarize(reviews, model)
print(result)
