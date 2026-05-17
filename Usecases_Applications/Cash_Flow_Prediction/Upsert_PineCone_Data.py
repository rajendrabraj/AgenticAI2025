import os
import logging
import warnings
from dotenv import load_dotenv, find_dotenv

# Find the .env file, searching upwards in the directory tree
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Now you can access environment variables
print(f"Path to .env file: {dotenv_path}")

pinecone_api_key = os.getenv("PINECONE_API_KEY", "") or os.getenv("PINE_CONE_API_KEY", "")
openai_api_key = os.getenv("OPENAI_API_KEY", "")
index_name = os.getenv("PINECONE_INDEX_NAME", "support-kb")
#index_host = os.getenv("PINECONE_INDEX_HOST", "")

index_host ="https://support-kb-yiy5ibb.svc.aped-4627-b74a.pinecone.io"

pinecone_environment = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
#vector_dimension = int(os.getenv("PINECONE_VECTOR_DIMENSION", "1536"))

vector_dimension= int("3072")  # For OpenAI's text-embedding-3-small model


warnings.filterwarnings("ignore")

print(f"PINECONE_API_KEY: {'SET' if pinecone_api_key else 'MISSING'}")
print(f"OPENAI_API_KEY: {'SET' if openai_api_key else 'MISSING'}")
print(f"PINECONE_INDEX_NAME: {index_name}")
print(f"PINECONE_INDEX_HOST: {'SET' if index_host else 'MISSING'}")
print(f"PINECONE_ENVIRONMENT: {pinecone_environment}")

if not pinecone_api_key:
    raise ValueError("PINECONE_API_KEY is required in the environment or .env file.")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is required in the environment or .env file.")

try:
    import pinecone
except Exception as exc:
    raise ImportError(
        "Unable to import Pinecone. Remove any old pinecone-client installation and install the official package with `pip install pinecone`."
    ) from exc

from langchain_openai import OpenAIEmbeddings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

pinecone_client = pinecone.Pinecone(api_key=pinecone_api_key, environment=pinecone_environment)
if index_host:
    index = pinecone_client.Index(host=index_host)
else:
    index = pinecone_client.Index(name=index_name)

#embeddings = OpenAIEmbeddings()

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")  # 3072 dims


documents = [
    {"id": "id1", "text": "Refund policy: Users can request refund within 7 days of duplicate charge."},
    {"id": "id2", "text": "Subscription billing issues can be resolved by verifying transaction ID."},
    {"id": "id3", "text": "Technical issues should be escalated if unresolved within 24 hours."},
    {"id": "id4", "text": "Personal data must never be shared with unauthorized users."},
    {"id": "id5", "text": "Refund policy: Users can request refund within 14 days of duplicate charge."},
    {"id": "id6", "text": "Subscription billing issues can be resolved by verifying transaction ID."},
    {"id": "id7", "text": "Technical issues should be escalated if unresolved within 48 hours."},
    {"id": "id8", "text": "Personal data must never be shared with unauthorized users."},
    {"id":"id9", "text":"The courier service delivering your order usually tries to deliver on the next business day in case you miss a delivery. You can check your SMS for more details on when the courier service will try to deliver again."},
    {"id":"id10", "text":"Couriers make sure that the delivery is re-attempted the next working day if you can't collect your order the first time."},
    {"id":"id11", "text":"On the rare occasion that your order is delayed, please check your email & messages for updates. A new delivery timeframe will be shared with you and you can also track its status by visiting My Orders."},
    {"id":"id12", "text":"Sellers usually ship orders 1-2 business days before the delivery date so that they reach you on time. In case your order hasn't been shipped within this time please contact our Customer Support so that we can look into it."},
    {"id":"id13", "text":"As per company policy, a shipment can't be opened before delivery, but you can accept the shipment and get in touch with us later in case you have any concerns."},
    {"id":"id14", "text":"An e-mail & SMS will be sent once you've successfully placed your order. We'll also let you know as soon as the seller ships the item(s) to you along with the tracking number(s) for your shipment(s). You can track your orders from the 'My Orders' section on your Flipkart account. \n"},
    {"id":"id15", "text":"Orders will be delivered by the date you see on the product page for your location."},
    {"id":"id16", "text":"The courier service delivering your order are responsible for making sure that your order reaches you within the delivery date. Rest assured, you'll get an SMS once your shipment is out for delivery."},
    {"id":"id17", "text":"The courier service will contact you for delivery of your order. Please check your SMS for more details."},
    {"id":"id18", "text":"Courier services usually take upto 24 hours to activate tracking for an order once it's shipped. Please check again after the mentioned time frame."},
    {"id":"id19", "text":"Sellers send a hard copy of the invoice in the shipments. A soft copy is also emailed to you within 24 hours of delivery in the delivery confirmation email sent to your registered email ID. You can also visit My Account › My Orders page to get invoices for your orders."},
    {"id":"id20", "text":"You can easily send invoices to your email ID from your Flipkart account. To do so, visit My Account › Orders, choose the order for which you'd like the invoice for and click on the 'E-mail Invoice' option."},
    {"id":"id21", "text":"To make sure that you have a smooth and hassle-free experience, the installation is automatically arranged for your product by the seller within 2-5 business after the item is delivered. You will also get an SMS with the exact installation details after delivery."},
    {"id":"id22", "text":"Your product will be installed by the brand's authorised service partner. Rest assured, the warranty for the product will not be affected when an item is installed by the authorised partners."},
    {"id":"id23", "text":"All orders are shipped by sellers through courier services who deliver the packages to your doorstep or the nearest pick-up store if the option is selected."},
    {"id":"id24", "text":"Availability of the 'Cash on Delivery' payment mode depends on the courier services delivering to your location. Please enter your pincode on the product page to check if this payment mode is available at your location. Courier service providers also have limits on the amount you can pay through cash on delivery based ..."},
    {"id":"id25", "text":"You can see the respective seller's Returns policy on the product page."},
    {"id":"id26", "text":"Sometimes items have to be sourced by sellers from their international partners. Such items have the tag 'Imported' on the product page and can take at least 10 or more days to be delivered."},
    {"id":"id27", "text":"To place an order, please follow these steps: 1. Select the product you'd like to buy and 'Check Availability at' your preferred pincode2. Add products to your cart or just hit 'Buy Now' 3. Choose or 'Add delivery address'. Use a preferred payment mode and confirm the order"},
    {"id":"id28", "text":"You can contact our Customer Support team with the details and we will get in touch with the courier service provider to resolve your complaint."},
    {"id":"id29", "text":"Please contact our Customer Support with the service centre details so that we can look into this."},
    {"id":"id30", "text":"Your order will get delivered on or before the delivery date promised at the time of placing the order."},
    {"id":"id31", "text":"Business days are otherwise known as working days of the week. The expected date of delivery is calculated based on business days. Typically, these include Monday through Saturday. Public holidays and Sundays are usually not considered."},
    {"id":"id32", "text":"Sellers generally procure and ship the items within the time specified on the product page. Business days exclude public holidays and Sundays. Estimated delivery time depends on the following factors: - The seller offering the product- Product's availability with the seller- The destination to which you want the order ..."},
    {"id":"id33", "text":"Groceries on Flipkart are available from top brands such as HUL, P&G, ITC etc. which are renowned for their quality products. Seller also checks the freshness of groceries when they receive the stock from vendors and before the dispatch of items in order to ensure that only the best produce and packaged groceries reach..."},
    {"id":"id34", "text":"If your tracking information shows that your package was delivered, but you can't find it: Check your phone for any notification about attempted delivery.See if any of your neighbours/friends/relatives/house owner/security guard has collected your product on your behalf.Wait until the end of the day— sometimes packages..."},
    {"id":"id35", "text":"Sometimes, a package cannot be delivered due to one of the following reasons: Incorrect Address: If the address is incorrect or outdated, the package is usually returned to the seller by the courier service provider or the unintended recipient. Please double-check your address carefully when placing a new order. To rem..."},
    {"id":"id36", "text":"The different order statuses are as mentioned below: Approved: Order you have placed for an item is confirmed by the seller Ready to Ship: Your item is packed and ready for pick up by a courier service provider Dispatched: Your item has been picked up from the seller by the courier service provider and is on its way ..."},
    {"id":"id37", "text":"Through GSTIN Invoicing feature customers can enter their business entity details and GSTIN associated with the business entity in order to receive a tax invoice containing these details to claim input tax credit. Please note, this is available on select products for business purchases sold by participating sellers."},
    {"id":"id38", "text":"Customers that have GSTIN registered for their business entity can avail this feature. Please note that this is currently available on select products for business purchases sold by participating sellers. Customers can enter GSTIN and business entity name while placing the order to receive a tax invoice containing th..."},
    {"id":"id39", "text":"Visit My Orders to check the status of your replacement. In most locations, the replacement item is delivered to you at the time of pick-up. In all other areas, the replacement is initiated after the originally delivered item is picked up. Please check the SMS & email we send you for your replacement request for more d..."},
    {"id":"id40", "text":"The following table contains a list of products that are not eligible for returns as per the seller’s Returns Policy:   Category Products that can’t be returned Auto Accessories Additives, Air Fresheners, Brighteners, Cleaners, Bike/Car Stickers, Degreasers, Dent/Scratch Removers, Filler Putty, Headlight Vi..."},
    {"id":"id41", "text":"No, sellers will not be able to accept returns after the time period mentioned in the seller's Returns Policy."},
    {"id":"id42", "text":"Yes, the freebie has to be returned along with the product."},
    {"id":"id43", "text":"You can raise a request to return your items with these simple steps: 1. Log into your Flipkart account 2. Go to My Orders 3. Click on 'Return' against the item you wish to return or exchange 4. Fill in the details and raise a return request Once you raise a request, you'll get an email and SMS confirming that your..."},
    {"id":"id44", "text":"A greyed out and disabled 'Cancel' button can mean any one of the following:1. The item has been delivered alreadyOR2. The item is non-refundable (e.g. Gift Card)"},
    {"id":"id45", "text":"The Buyer Protection policy mediates buyer-seller disputes. In case a seller declines your request for a return of an item and you are not convinced with the reason given, you can write to us at resolution@flipkart.com for Buyer Protection. You can dispute the resolution that the seller has shared for your issue until ..."},
    {"id":"id46", "text":"You can get in touch with the brand or an authorised service centre of the brand to claim the warranty for your product (wherever applicable)."},
    {"id":"id47", "text":"To return/exchange your order, follow these simple steps: 1. Go to My Orders 2. Choose the item you wish to return or exchange 3. Fill in the details 4. Choose Request Return."},
    {"id":"id48", "text":"Sellers cannot accept returns of item(s) in the following cases: 1. When an item is damaged because of use or when it is not in the same condition as you received it2. When any consumable item has been used or installed3. When anything is missing from the package you've received including price tags, labels, original p..."},
    {"id":"id49", "text":"You can visit 'My Orders' to know the status of your refund. For orders cancelled before shipping, refunds are processed immediately. If the order has been shipped. refund will be processed as soon as the courier service provider confirms the return of the item(s)."},
    {"id":"id50", "text":"The different refund modes available are: 1. PhonePe Wallet - available for orders with select sellers. You will get this option for eligible orders during cancellation 2. Back to source - available for orders with all sellers. The amount is refunded to the payment mode that was originally used to pay for the order 3...."},
    {"id":"id51", "text":"Refunds are given when: - The seller cannot provide a replacement- A dispute has been ruled in your favour in-line with Buyer Protection- Sellers allow refunds on select categories under certain conditions Please check the seller's Returns Policy on the product page for more details."},
    {"id":"id52", "text":"The sellers' return policies don't support the return of item(s) ordered wrongly. You can refer the respective seller's Returns policy on the product page."},
    {"id":"id53", "text":"You can request for the item to be replaced by visiting 'My Orders'. Use the 'Return' option & fill out the details of the issue so that we can help you."},
    {"id":"id54", "text":"If the pincode of the new address is serviceable for pick-up, the address can be changed while creating the return. The address cannot be changed in case the new address is not serviceable."},
    {"id":"id55", "text":"When pickup facility is not available for your location as per the courier service providers, you may be asked to ship the item back to the seller. Since the seller can arrange for a refund or a replacement only after the item reaches them, please make sure that the item is sent to the address mentioned in the return r..."},
    {"id":"id56", "text":"Once your return or replacement or exchange request is accepted, the pickup of the originally delivered product will be scheduled. An SMS with more details will be sent to you on the day of the pickup. In cases where pickup service is not available from the courier service providers at your location, you may be asked t..."},
    {"id":"id57", "text":"You can now track the status of your return easily right from your Flipkart account or mobile app. Just visit the 'My Orders' page to see its status along with the date of pick-up and status of your refund if applicable. You will also receive an email & SMS with the details of your return."},
    {"id":"id58", "text":"You may visit 'My Orders' to check the status of your replacement. In most locations, the replacement item is delivered to you at the time of pick-up. In all other areas, the replacement is initiated after the originally delivered item is picked up. Please check the SMS & email that will be sent to you for your replace..."},
    {"id":"id59", "text":"If you have received a mail from us confirming your refund request, it means that the refund has been initiated. You can also contact your bank with the ARN you would have received for an update on the status of your refund. In the rare event of the amount not being credited by the date promised, you can contact us as ..."},
    {"id":"id60", "text":"The refund timelines will depend on the payment modes as listed below: Debit card - 7-9 Business days Credit - 7-9 Business days Netbanking - 3-7 business days COD - IMPS, 1 Business days EMI (Standard+No cost+Debit card) - 7- 9 Business days Flipkart Pay Later - 24 to 48 hours Gift Card - 24 hours PhonePe: PhonePe..."},
    {"id":"id61", "text":"For orders placed using 'Cash on Delivery' as the payment mode, refunds can be processed to your bank account via Immediate Payment Service (IMPS). You can update the details of the bank account where you would like to receive the refund while creating the return request for an item. You will need to update following i..."},
    {"id":"id62", "text":"Please follow the below-mentioned steps on our website to upload a scanned copy of the receipt from the courier service provider so that we can request the seller for a reimbursement: Go to Flipkart Help Center and select the relevant order for which the refund has been requested From the issue types, choose 'Others..."},
    {"id":"id63", "text":"For your 'Cash on Delivery order, you will receive the refund in the form of NEFT. Please update your bank account details after you choose this option."},
    {"id":"id64", "text":"Cancellation of item(s) in an order happens immediately if the order hasn't been shipped yet by the seller. If your order has been shipped, it will be cancelled as soon as the courier service confirms that the shipment is being returned to the seller. Orders from certain categories cannot be cancelled after 24 hours, p..."},
    {"id":"id65", "text":"During pick-up, your product will be checked for the following conditions:   Correct Product IMEI/ name/ image/ brand/ serial number/ article number/ bar code should match and MRP tag should be undetached and clearly visible. Complete Product All in-the-box accessories (like remote control, starter kits, i..."},
    {"id":"id66", "text":"If your return requests are significantly higher than most customers, a return fee will apply to your order. This is levied to compensate sellers for the huge losses they incur as part of each return request. In case of an issue with the item, you can choose to exchange or replace it instead of returning it to avoid ..."},
    {"id":"id67", "text":"The return fee is determined based on the selling price of the product. Lower the selling price of the product, lower the return fee and vice versa."},
    {"id":"id68", "text":"With Flipkart’s credit card EMI option, you can choose to pay in easy installments of 3, 6, 9, 12, 18, or 24 months, with credit cards from the following banks: HDFC Citi ICICI Kotak Axis Induslnd SBI Standard Chartered HSBC *18 & 24 months EMI options are available from s..."},
    {"id":"id69", "text":"You can write to corporatesales@flipkart.com for your corporate gifting requirements."},
    {"id":"id70", "text":"You can specify a card label at the time of saving a card on Flipkart through the 'My Account' section. You can also add/edit the label anytime through 'My Saved Cards' in the 'My Account' section on Flipkart."},
    {"id":"id71", "text":"A card label is a name you give to your card while saving it on Flipkart. This helps in identifying the card at the time of making a payment. Even if you don't specify a card label, you can still identify the card by the first 2 and last 4 digits of the card number which are visible to you when the saved card is show..."},
    {"id":"id72", "text":"The 'Save Card' option lets you save your credit/debit cards on your Flipkart account. This helps you complete your transactions in a quick and easy way."},
    {"id":"id73", "text":"Online payments are monitored by our systems for any suspicious activity and some transactions are verified through extensive checks if we find that they are not authorised by the owner of the card. When we're not able to rule fraud out in rare cases, the transaction is kept on hold and we ask the shopper to share rele..."},
    {"id":"id74", "text":"When you're prompted to choose a payment method for your order, select EMI and then choose the bank and the plan you would prefer. Enter your credit card and follow the prompts. Once the payment is authorised, your order will be processed and shipped. You'll need to pay the total amount in the predetermined number o..."},
    {"id":"id75", "text":"If you have paid for your order using the EMI payment mode, the full amount will be charged to your card the day of the transaction. Within 7 days, you will see a credit for the full amount. The first EMI charge will occur subsequently. If your card's billing date falls within those 7 working days, you need to pay only..."},
    {"id":"id76", "text":"You can get in touch with your card issuing bank to know about EMI transaction charges as they may vary across banks."},
    {"id":"id77", "text":"You will see the actual interest rates and the amount charged by the bank for your credit card EMI plan during checkout after choosing the EMI payment method while placing your order."},
    {"id":"id78", "text":"EMI is available for Credit cards from the following banks: ICICI Citi SBI HDFC Kotak Standard Chartered HSBC Axis IndusInd Please check the specific product page for more details as this list is updated frequently."},
    {"id":"id79", "text":"You can choose to pay on Flipkart with any Visa, MasterCard or American Express credit card issued in India."},
    {"id":"id80", "text":"You can choose to pay for your order on Flipkart with any Visa, MasterCard or Maestro Debit Card."},
    {"id":"id81", "text":"The availability of Cash on Delivery option depends on factors like the delivery pincode, type of products etc. Please enter your pincode on the product page to check if CoD is available at your location. If this option is available for your pincode, you can shop for products up to ₹49,999 using this."},
    {"id":"id82", "text":"You can get a 3D Secure password by registering your Credit/Debit Card on your bank's website."},
    {"id":"id83", "text":"Your saved cards can be seen when you choose the credit or debit card option to pay for your order. Enter the CVV number of that card (we do not store it) and click on the 'Pay' button. You'll also have to enter the card's 3D Secure password to complete the transaction."},
    {"id":"id84", "text":"You can choose to pay for an order using any of the below methods: Cash on Delivery Net Banking Gift Card PhonePe Wallet Visa, MasterCard, Maestro and American Express Credit or Debit cards issued in India and 21 other countries To know more about payments, click here: http://www.flipkart.com/s/help/payments"},
    {"id":"id85", "text":"You can directly pay for your order at the pickup outlet for Cash on Delivery orders."},
    {"id":"id86", "text":"You may choose the credit card or debit card option to pay during checkout and enter the details when prompted. You would need to keep your card number, expiry date, three digit CVV number ready, which you can find on your card. For added security, you'll also need to use your card's online password that is verified by..."},
    {"id":"id87", "text":"The 3D Secure password is something that only you would know, ensuring no one else can use your card to shop online."},
    {"id":"id88", "text":"Yes. Even if you've saved your card details on Flipkart, you always have the option to use any other credit/debit card to pay."},
    {"id":"id89", "text":"A 3D Secure password adds an extra layer of security through identity verification for your online Credit & Debit card transactions (VISA & MasterCard)."},
    {"id":"id90", "text":"You can shop up to Rs. 49,999 using Cash on Delivery (CoD) option."},
    {"id":"id91", "text":"Cash on Delivery is a mode of payment in which you can pay cash at the time of delivery of your order. You can also pay using a credit card/ debit card if the Courier Executive carries a swiping machine."},
    {"id":"id92", "text":"It's quicker. You can save the hassle of typing in the complete card information every time you shop on Flipkart by saving your card details. You can make your payment by selecting the saved card of your choice at checkout. While this is obviously faster, it is also very secure."},
    {"id":"id93", "text":"We only store your card number, cardholder name and card expiry date. We do not store your card's CVV number or the 3D secure password. Flipkart stores your card information only when you select the option.We only store your card number, cardholder name and card expiry date. We do not store your card's CVV number or th..."},
    {"id":"id94", "text":"Yes, you can delete your saved cards at any given time."},
    {"id":"id95", "text":"As of now, you can save upto 10 cards using the 'Save Card' option."},
    {"id":"id96", "text":"You can save any credit or debit VISA, MasterCard, Maestro or American Express card issued by a bank in India."},
    {"id":"id97", "text":"Your card is saved automatically when you make a successful payment by entering the card details while purchasing on Flipkart. Alternatively, you can also save your card by navigating to 'My Accounts > Payments > My Saved Cards'. To save the card you'll need the card number and the expiry date. You can also add a card ..."},
    {"id":"id98", "text":"You can view your saved cards by selecting the credit/debit card payment option at checkout. Select a saved card that you wish to use to make the payment. Enter the CVV number of that card (we do not store it) and click the 'Pay' button to initiate your payment. You will also have to enter the card's 3D Secure password..."},
    {"id":"id99", "text":"Yes. Even if you have saved your card on Flipkart, you always have the option to use any other credit/debit card for making a payment."},
    {"id":"id100", "text":"You can delete your saved card information on Flipkart from the 'My Account' section. Go to 'My Account > Payments > My Saved Cards' and you will be able to see your saved card(s). You can then click on 'Remove this card'."},
    {"id":"id101", "text":"A card label is the name you give to your card while saving it on Flipkart. This helps in identifying the card at the time of making a payment. Even if you do not specify a card label, you will still be able to identify the card by the first 2 and last 4 digits of your card number which will be visible to you when the ..."},
    {"id":"id102", "text":"You can specify a card label at the time of saving a card on Flipkart through the My Account section. If you did not specify any card label at the time of saving the card, you can still add/edit the label anytime through the My Saved Cards menu in the My Account section on Flipkart."},
    {"id":"id103", "text":"You should have a registered account with Flipkart to which you should be logged in. Due to security reasons, this feature is not available during guest checkout."},
    {"id":"id104", "text":"Yes, if your saved credit card is eligible for your Bank's EMI program then you can use it for making an EMI payment."},
    {"id":"id105", "text":"If you choose to save your card at the time of making the payment, then the only time your card may not get saved is when the payment fails due to card being invalid. If the payment was successful and the card was not saved, then you may contact us and we will help you out."},
    {"id":"id106", "text":"If you typed an incorrect card number, name or card expiry date, you need to first delete the entered details by clicking on \"Remove this card\" and then add the card again with the correct details."},
    {"id":"id107", "text":"Absolutely! Any cards that you save on Flipkart's website can be used on Flipkart app and mobile site as well. You can also save cards through your mobile and use them on Flipkart's website."},
    {"id":"id108", "text":"You can manage these cards from the 'Saved Cards' section on PhonePe or Flipkart. If you wish to delete a card from both PhonePe and Flipkart, you need to perform this operation independently in both the applications."},
    {"id":"id109", "text":"Yes, you can use your Debit/Credit Card to shop on our mobile app, website, and mobile site too!"},
    {"id":"id110", "text":"Cash on Delivery payments cannot be combined with other payments modes."},
    {"id":"id111", "text":"Since payment modes cannot be changed after an order is placed, to cancel your EMI, your order will need to be cancelled. Certain items cannot be cancelled after 24 hours of placing the order."},
    {"id":"id112", "text":"No, the refund for an order placed using the Bajaj Finserv payment mode can only be done to the bank account linked to the Bajaj Finserv EMI Card."},
    {"id":"id113", "text":"No, a down payment is not required for buying an item using the Bajaj Finserv EMI option."},
    {"id":"id114", "text":"You can check the eligibility and process of getting a Bajaj Finserv No Cost EMI card on their website: www.bajajfinserv.in/finance."},
    
]

vectors = []
for record in documents:
    emb = embeddings.embed_query(record["text"])
    vectors.append((record["id"], emb, {"text": record["text"]}))

print(f"Upserting {len(vectors)} vectors into Pinecone index '{index_name}'...")
response = index.upsert(vectors=vectors)
print("Upsert response:", response)
logging.info("Pinecone upsert completed.")
