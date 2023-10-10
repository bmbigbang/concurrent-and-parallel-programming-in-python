This project demonstrates a simple example of utilizing python's concurrency and parallel processing capabilities to
read stock market data from yahoo finance website. This allows us to demonstrate the fine detail of what goes on in the 
background and how we can optimize for time as well as introduce robustness and error handling.

Note that a cookie may be needed for the yahoo finance requests to work correctly. See the header object of the 
`get_price` function in `YahooFinanceWorker.py`.

Run the `init_database.py` command to create the database and table to for the workers.