import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def tier_for(amount):
    if amount >10000:
        return "Lead Benefactor"
    elif amount >=1000:
        return "Major donor!"
    elif amount >=100:
        return "Generous Supporter"
    else:
        return "Valued friend"

def thank_you_message(name, amount, note, tone):
    tier = tier_for(amount)
    
    system_prompt = (
        "You are a warm, sincere fundraising specialist for an NGO. "
        f"Write thank-you letters in a {tone} tone, never templated. "
        "Three short paragraphs. Must use only 'The Team' for sign off. Just one line of text."
    )
    
    user_prompt = f"""
    Write a thank-you letter for a donor with these details:
    - Name: {name}
    - Donation amount: ${amount}
    - Donor tier: {tier}
    - Note: {note}
    - Tone: {tone}
    The letter should acknowledge their specific contribution and tier without being formulaic.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    return response.choices[0].message.content

donors = [
    ["Madina", 10000, "First-time corporate donor; wants impact reports."],
    ["Aizada", 12000, "Has volunteered with us for 5 years." ],
    ["Sam", 250, "New donor; wants to know more about our work."],
    ["Aigerim", 1500, "Long-time donor; enjoys our newsletters."],
    ["Bakyt", 50, "Our own employee; donates consistently."],
    ["Meerinm", 5000, "Strong believer of the work we do."],
    ["Erlan", 75, "New donor; wants to volunteer with us."],
]

tone = "formal"
total = 0
letter_count = 0
os.makedirs("letters", exist_ok=True)
sorted_donors = sorted(donors, key=lambda x: x[1], reverse=True)

for donor in sorted_donors:
    name = donor[0]
    amount = donor[1]
    note = donor[2]
    message = thank_you_message(name, amount, note, tone)
    print(message)
    print("---")
    total = total + amount
    letter_count = letter_count + 1
    with open(f"letters/{name}.txt", "w") as f:
        f.write(message)

print(f"Generated {letter_count} letters totaling ${total}")




