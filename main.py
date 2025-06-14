from api import PaystackAPI
import asyncio


def main():
    """
    Main function to run the Paystack API example.
    """
    
    # Initialize the Paystack API client
    # Replace with your actual secret key
    secret = "sk_test_1234567890abcdef1234567890abcdef"
    paystack = PaystackAPI()
    
    # Example usage
    
    # create a customer
    # asyncio.run(paystack.create_customer())
    
    # generate payment request
    # asyncio.run(paystack.create_payment_request())
    
    # send notification for payment request
    # asyncio.run(paystack.send_notification())
    
    # initialize a transaction (generates a payment link)
    # asyncio.run(paystack.initialize_transaction())
    
    # create a recipient
    # asyncio.run(paystack.create_transfer_recipient(recipient_name="Demiz"))
    
    # initialize money transfer (payout)
    # asyncio.run(paystack.initialize_transfer())
    
    # finalize money transfer (note: used only when Paystack is handling transfer verification instead of your app)
    # asyncio.run(paystack.complete_transfer(otp_code="434589"))
    
    # verify payment
    # asyncio.run(paystack.verify_payment())
    
    # list supported countries
    # asyncio.run(paystack.list_countries())
    
    # list supported banks
    asyncio.run(paystack.list_banks())
    
    return paystack.DATA



if __name__ == "__main__":
    _ = main()
    print(_)