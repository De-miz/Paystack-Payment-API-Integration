import aiohttp



PAYSTACK_SECRET_KEY = "sk_test_87b11c444fb666ccd8a4ac6b790880ec7a471501"

class PaystackAPI:
    def __init__(self, secret_key=PAYSTACK_SECRET_KEY, proxy_url=None) -> None:
        # print("This is the paystack secret key:", secret_key)
        self.proxy_url = proxy_url
        self.SECRET_KEY = secret_key
        self.STATUS = False
        self.MESSAGE = ""
        self.DATA = {}
        self.PROXY_URL = ""
    
    # Subscribing to a youtube channel    
    async def create_customer(self, email:str="eddieblapoh@gmail.com", phone:str="+233530972529", first_name:str="Eddie2", last_name:str="Kweh"):
        payload = {
            "email": email, 
            "phone": phone, 
            "first_name": first_name, 
            "last_name": last_name,
        }

        headers = {
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {self.SECRET_KEY}"
        }
        
        parameters={}

        connector = aiohttp.TCPConnector(ssl=False)

        try:
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post("https://api.paystack.co/customer", json=payload, headers=headers, params=parameters, proxy=self.proxy_url) as response: # session.get() will have a second arg proxy=self.PROXY_URL when in production
                    data = await response.json()
                    self.DATA = data
                    if response.status:
                        if data.get('error'):
                            pass
                    else:
                        print(data, 'somethings wrong', response)
        except Exception as error:
            print("Error occurred: ", error)
        finally:
            await session.close()


    async def create_payment_request(self, customer_id_or_code:str="CUS_6e8ktlzuem4vhz4", amount:float|int=1):
        payload = {
            "customer": customer_id_or_code, 
            "amount": amount
        }

        headers = {
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {self.SECRET_KEY}"
        }
        
        parameters={}

        connector = aiohttp.TCPConnector(ssl=False)

        try:
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post("https://api.paystack.co/paymentrequest", json=payload, headers=headers, proxy=self.PROXY_URL) as response: # session.get() will have a second arg proxy=self.PROXY_URL when in production
                    data = await response.json()
                    self.DATA = data
                    if response.status:
                        if data.get('error'):
                            pass
                    else:
                        print(data, 'somethings wrong', response)
        except Exception as error:
            print("Error occurred: ", error)
        finally:
            await session.close()
                    
                    
    async def send_notification(self, payment_request_code:str="PRQ_mvqwhk3px3ox0nk"):
        payload = {
            "code": payment_request_code
        }
        
        headers = {
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {self.SECRET_KEY}"
        }
        
        parameters={"code": payment_request_code}

        connector = aiohttp.TCPConnector(ssl=False)

        try:
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post(f"https://api.paystack.co/paymentrequest/notify/:{payment_request_code}", headers=headers, params=parameters, proxy=self.PROXY_URL, json=payload) as response: # session.get() will have a second arg proxy=self.PROXY_URL when in production
                    data = await response.json()
                    self.DATA = data
        except Exception as error:
            print("Error occurred: ", error)
        finally:
            await session.close()
                
                     
    async def initialize_transaction(self, email:str="eddieblapoh@gmail.com", amount:float|int=1, currency:str="GHS", callback_url:str="", channel:str="mobile_money", charge:float|int=0):
        """
        Initializes a payment transaction with Paystack.
        Args:
            email (str, optional): The customer's email address. Defaults to "eddieblapoh@gmail.com".
            amount (int, optional): The amount to be paid. Defaults to 1.
            currency (str, optional): The currency of the transaction. Defaults to "GHS".
            callback_url (str, optional): The URL to which Paystack will redirect after a successful transaction.
                Defaults to 'callback_url'.
            channel (str, optional): The payment channel to use. Defaults to "mobile_money".
            charge (int, optional): The payment charge. Defaults to 0.
        Returns:
            None. The method sets the following attributes:
                self.DATA (dict): The data returned by Paystack, containing authorization URL, access code, and reference.
                self.STATUS (bool): True if the transaction was initialized successfully, False otherwise.
                self.MESSAGE (str): An error message if the transaction failed.
        Raises:
            aiohttp.ClientError: If there is an error during the API request.
        """
        
        default_curr_amount = round(amount, 2)
        
        
        body = { # body parameters
            "email": email, 
            "amount": round(default_curr_amount * 100, 2), # Amount to pay in kobo if currency is NGN and pesewas if currency is GHS.
            "currency": currency,
            "channels": [channel], # list of the payment methods e.g. ["card", "bank", "ussd", "qr", "mobile_money", "bank_transfer", "eft"]
            "callback_url": callback_url, 
            "metadata": {"payment_fee": charge}, # metadata is a custom parameter
        }
        
        headers = {
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {self.SECRET_KEY}"
        }

        connector = aiohttp.TCPConnector(ssl=False)

        try:
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post("https://api.paystack.co/transaction/initialize", headers=headers, json=body, proxy=self.PROXY_URL) as response: # session.get() will have a second arg proxy=self.PROXY_URL when in production
                    data = await response.json()
                    self.DATA = data 
                    if response.status:
                        self.STATUS = True
                        self.DATA = data 
                    else:
                        self.STATUS = False
                        self.MESSAGE = data.get("message")
        except Exception as error:
            print("Error occurred: ", error)
        finally:
            await session.close()
         
                    
    async def create_transfer_recipient(self, currency:str="GHS", account_number:str="0500000000", bank_code:str="MTN", recipient_type:str="mobile_money", recipient_name=""):
        
        body = { # body parameters
            "type": recipient_type, # same as bank type e.g. ghipss, mobile_money, nuban, basa
            "name": recipient_name, # recipient's name is blank at default
            "account_number": account_number, # either bank account number or mobile money number
            "bank_code": bank_code, 
            "currency": currency,
        }
        
        headers = {
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {self.SECRET_KEY}"
        }

        connector = aiohttp.TCPConnector(ssl=False)

        try:
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post("https://api.paystack.co/transferrecipient", headers=headers, json=body, proxy=self.PROXY_URL) as response: # session.get() will have a second arg proxy=self.PROXY_URL when in production
                    data = await response.json()
                    self.DATA = data 
                    if response.status:
                        self.STATUS = True
                    else:
                        self.STATUS = False
                        self.MESSAGE = data.get("message")
                    return data
        except Exception as error:
            print("Error occurred: ", error)
        finally:
            await session.close()
            
                       
    async def initialize_transfer(self, recipient_code:str="RCP_yf3stblbl2teikx", currency:str="GHS", amount:float=10000):
        '''Initialize a money payout/transfer to a recipient'''
        
        body = { # body parameters
            "currency": currency,
            "source": "balance", # Where should we transfer from? Only balance for now
            "reason": "Converting coinns to cash", 
            "amount":amount * 100, # Amount to transfer in kobo if currency is NGN and pesewas if currency is GHS.
            "recipient": recipient_code,
        }
        
        headers = {
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {self.SECRET_KEY}"
        }

        connector = aiohttp.TCPConnector(ssl=False)

        try:
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post("https://api.paystack.co/transfer", headers=headers, json=body, proxy=self.PROXY_URL) as response: # session.get() will have a second arg proxy=self.PROXY_URL when in production
                    data = await response.json()
                    self.DATA = data 
                    if response.status:
                        self.STATUS = True
                    else:
                        self.STATUS = False
                        self.MESSAGE = data.get("message")
                    return data
        except Exception as error:
            print("Error occurred: ", error)
        finally:
            await session.close()
            
                   
    async def complete_transfer(self, transfer_code:str="TRF_o34dskvrtz5ahn9q", otp_code:str=""):
        '''complete a money payout/transfer to a recipient'''
        
        body = { # body parameters
            "transfer_code": transfer_code, 
            "otp": otp_code, # otp code sent to user phone number
        }
        
        headers = {
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {self.SECRET_KEY}"
        }

        connector = aiohttp.TCPConnector(ssl=False)

        try:
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post("https://api.paystack.co/transfer/finalize_transfer", headers=headers, json=body, proxy=self.PROXY_URL) as response: # session.get() will have a second arg proxy=self.PROXY_URL when in production
                    data = await response.json()
                    self.DATA = data 
                    if response.status:
                        if data.get("status"):
                            self.STATUS = True
                    else:
                        self.STATUS = False
                    return data
        except Exception as error:
            print("Error occurred: ", error)
        finally:
            await session.close()
                
                     
    async def verify_payment(self, reference:str="f707qojdhu") -> None:
        
        headers = {
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {self.SECRET_KEY}"
        }

        connector = aiohttp.TCPConnector(ssl=False)

        try:
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(f"https://api.paystack.co/transaction/verify/{reference}", headers=headers, proxy=self.PROXY_URL) as response: # session.get() will have a second arg proxy=self.PROXY_URL when in production
                    data = await response.json()
                    self.DATA = data
                    if response.status:
                        if data.get('data', {}).get('status') == "success": # if payment was successfully made
                            self.STATUS = True
                        else:
                            self.STATUS = False
                    else:
                        self.STATUS = False 
                        self.MESSAGE = "Unknown error occured"
        except Exception as error:
            print("Error occurred: ", error)
        finally:
            await session.close()
                
                
    async def list_countries(self):
        
        headers = {
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {self.SECRET_KEY}"
        }

        connector = aiohttp.TCPConnector(ssl=False)

        try:
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get("https://api.paystack.co/country", headers=headers, proxy=self.PROXY_URL) as response: # session.get() will have a second arg proxy=self.PROXY_URL when in production
                    data = await response.json()
                    self.DATA = data
                    return data
        except Exception as error:
            print("Error occurred: ", error)
        finally:
            await session.close()
            
            
    async def list_banks(self, country:str="ghana", currency:str="GHS", type:str="mobile_money"):
        
        headers = {
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {self.SECRET_KEY}"
        }

        connector = aiohttp.TCPConnector(ssl=False)

        try:
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(f"https://api.paystack.co/bank?country={country}&currency={currency}&type={type}&use_cursor=true&perPage=100", headers=headers, proxy=self.PROXY_URL) as response: # session.get() will have a second arg proxy=self.PROXY_URL when in production
                    data = await response.json()
                    self.DATA = data
                    return data
        except Exception as error:
            print("Error occurred: ", error)
        finally:
            await session.close()
                