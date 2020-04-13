# simple algorithm based on moving averages crossover strategy.

# you don't need to call this function to run.
def initialize(context):
    set_benchmark(sid(24))
    # sid = stock id, used to call the stock id of a company. context is the main data set.
    context.aapl = sid(24)
    
    # schedule fucntion allow you to make trades every day, every week or every month.
    # this is how to call and run a function. does't behave like a normal python program. 
    schedule_function(ma_crossover_handling, 
                      date_rules.every_day(), 
                      time_rules.market_open(hours=1))
         
def ma_crossover_handling(context, data):
    hist = data.history(context.aapl, 'price', 50, '1d')
    # log data 
    log.info(hist.head())
    
    # calculating simple moving averages. 
    sma_50 = hist.mean()
    sma_20 = hist[-20:].mean()
    
    open_orders = get_open_orders()
    
    # ordering stocks. 
    # takes time to order the stocks. 1st order might take a minute and 2nd order executes even if the 1st order is not complete. 
    if sma_20 > sma_50:
        if context.aapl not in open_orders:
            # buys 100% of apple shares. 
            order_target_percent(context.aapl, 1.0)
    elif sma_50 > sma_20:
        if context.aapl not in open_orders:
            order_target_percent(context.aapl, -1.0)
        
    # track and plot your leverage
    record(leverage = context.account.leverage)
