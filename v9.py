from Dhan_Tradehull import Tradehull
import time
import json
import os
from datetime import datetime
from collections import deque, defaultdict
from flask import Flask, render_template, jsonify, send_from_directory, Response

# Your credentials
CLIENT_CODE = "1106534888"
TOKEN_ID = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQ3NjQ2MDMzLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNjUzNDg4OCJ9.TrT8U_uS3TEqqF23VGBgc1_SHk9f3S0e6yp_tbRdZ97A_93bZuYNcUul9JvGxme4_8bd3rvgyUnuzdNa9Y8QYA"

# Configuration
WATCHLIST = [




        "AARTIIND", "ABB", "ABCAPITAL", "ABFRL", "ACC", "ADANIENSOL", "ADANIENT", 
        "ADANIGREEN", "ADANIPORTS", "ALKEM", "AMBUJACEM", "ANGELONE", "APLAPOLLO", 
        "APOLLOHOSP", "APOLLOTYRE", "ASIANPAINT", "ASTRAL", "ATGL", "AUBANK", 
        "AUROPHARMA", "AXISBANK", "BAJAJ-AUTO", "BAJAJFINSV", "BAJFINANCE", 
        "BALKRISIND", "BANKNIFTY", "BEL", "BERGEPAINT", "BHARATFORG", "BHARTIARTL", 
        "BHEL", "BIOCON", "BPCL", "BSE", "BSOFT", "CAMS", "CDSL", "CESC", "CGPOWER", 
        "CHAMBLFERT", "CHOLAFIN", "CIPLA", "COALINDIA", "COFORGE", "COLPAL", "CONCOR", 
        "CROMPTON", "CUMMINSIND", "CYIENT", "DABUR", "DALBHARAT", "DEEPAKNTR", "DELHIVERY", 
        "DIVISLAB", "DIXON", "DLF", "DMART", "DRREDDY", "EICHERMOT", "ESCORTS", "EXIDEIND", 
        "FEDERALBNK", "FINNIFTY", "GAIL", "GLENMARK", "GODREJCP", "GODREJPROP", "GRANULES", 
        "GRASIM", "HAL", "HAVELLS", "HCLTECH", "HDFCAMC", "HDFCBANK", "HDFCLIFE", 
        "HEROMOTOCO", "HINDALCO", "HINDPETRO", "HINDZINC", "HUDCO", "ICICIGI", "ICICIPRULI", 
        "IEX", "IGL", "IIFL", "INDHOTEL", "INDIANB", "INDIGO", "INDUSINDBK", "INDUSTOWER", 
        "INFY", "INOXWIND", "IREDA", "JINDALSTEL", "JIOFIN", "JSL", "JSWENERGY", "JUBLFOOD", 
        "KALYANKJIL", "KEI", "KOTAKBANK", "KPITTECH", "LAURUSLABS", "LICHSGFIN", "LODHA", 
        "LTIM", "LUPIN", "M&M", "M&MFIN", "MANAPPURAM", "MARICO", "MARUTI", "MAXHEALTH", 
        "MCX", "MFSL", "MGL", "MIDCPNIFTY", "MOTHERSON", "MPHASIS", "MUTHOOTFIN", "NATIONALUM", 
        "NAUKRI", "NCC", "NESTLEIND", "NIFTY", "NTPC", "NYKAA", "OBEROIRLTY", "OFSS", "OIL", 
        "ONGC", "PATANJALI", "PAYTM", "PEL", "PERSISTENT", "PETRONET", "PFC", "PHOENIXLTD", 
        "PNBHOUSING", "POLICYBZR", "POLYCAB", "POONAWALLA", "POWERGRID", "PRESTIGE", "RAMCOCEM", 
        "RBLBANK", "RECLTD", "RELIANCE", "SAIL", "SBICARD", "SBILIFE", "SBIN", "SHRIRAMFIN", 
        "SIEMENS", "SOLARINDS", "SONACOMS", "SRF", "SUNPHARMA", "SUPREMEIND", "SYNGENE", 
        "TATACHEM", "TATACOMM", "TATACONSUM", "TATAELXSI", "TATAMOTORS", "TATAPOWER", 
        "TATASTEEL", "TATATECH", "TCS", "TECHM", "TIINDIA", "TITAGARH", "TITAN", "TRENT", 
        "TVSMOTOR", "ULTRACEMCO", "UNITDSPR", "UPL", "VBL", "VEDL", "VOLTAS", "WIPRO", 
        "ZOMATO", "ZYDUSLIFE"




]
UPDATE_INTERVAL = 1  # Update every 1 second
HISTORY_INTERVALS = [10, 20, 30, 40, 50, 60, 120, 240, 360, 480, 600]  # 10s to 10min

# Create a folder for static files if it doesn't exist
static_folder = "static"
os.makedirs(static_folder, exist_ok=True)

# Create an html file for the dashboard in the static folder
with open(os.path.join(static_folder, "index.html"), "w") as f:
    f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Futures Watchlist Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #1a1a1a;
            color: #f0f0f0;
        }
        .container {
            max-width: 95%;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #444;
            margin-bottom: 20px;
        }
        .title {
            font-size: 24px;
            font-weight: bold;
        }
        .update-info {
            font-size: 14px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            font-size: 14px;
        }
        th, td {
            padding: 8px 12px;
            text-align: left;
            border-bottom: 1px solid #444;
        }
        th {
            background-color: #333;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        .sticky-header {
            position: sticky;
            top: 0;
            background-color: #1a1a1a;
            z-index: 100;
            padding-bottom: 10px;
        }
        .tabs {
            display: flex;
            margin-top: 20px;
        }
        .tab {
            padding: 10px 20px;
            background-color: #333;
            cursor: pointer;
            border-radius: 5px 5px 0 0;
            margin-right: 5px;
        }
        .tab.active {
            background-color: #444;
            font-weight: bold;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        .positive {
            color: #4caf50;
        }
        .negative {
            color: #f44336;
        }
        .neutral {
            color: #bdbdbd;
        }
        .buy-dominant {
            color: #4caf50;
            font-weight: bold;
        }
        .sell-dominant {
            color: #f44336;
            font-weight: bold;
        }
        .equal {
            color: #bdbdbd;
        }
        .stock-row:hover {
            background-color: #2a2a2a;
        }
        .refresh-rate {
            margin-top: 15px;
        }
        .filters {
            display: flex;
            gap: 15px;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="sticky-header">
            <div class="header">
                <div class="title">Futures Watchlist Dashboard</div>
                <div class="update-info">
                    Last update: <span id="last-update">--:--:--</span> | 
                    Iteration: <span id="iteration">0</span>
                </div>
            </div>
            
            <div class="tabs">
                <div class="tab active" onclick="switchTab('bs-tab')">B/S Ratios</div>
                <div class="tab" onclick="switchTab('sb-tab')">S/B Ratios</div>
            </div>
            
            <div class="filters">
                <div>
                    <label for="min-bs-ratio">Min B/S Ratio:</label>
                    <input type="number" id="min-bs-ratio" min="0" step="0.1" value="0" onchange="applyFilters()">
                </div>
                <div>
                    <label for="min-change">Min % Change:</label>
                    <input type="number" id="min-change" min="-100" step="0.1" value="-100" onchange="applyFilters()">
                </div>
                <div>
                    <label for="search-stock">Search Stock:</label>
                    <input type="text" id="search-stock" onkeyup="applyFilters()">
                </div>
                <div class="refresh-rate">
                    <label for="refresh-interval">Refresh Every:</label>
                    <select id="refresh-interval" onchange="updateRefreshInterval()">
                        <option value="1000">1 second</option>
                        <option value="2000">2 seconds</option>
                        <option value="5000">5 seconds</option>
                        <option value="10000">10 seconds</option>
                    </select>
                </div>
            </div>
        </div>
        
        <div id="bs-tab" class="tab-content active">
            <table id="bs-table">
                <thead>
                    <tr>
                        <th>Stock</th>
                        <th>LTP</th>
                        <th>Change %</th>
                        <th>Buy Qty</th>
                        <th>Sell Qty</th>
                        <th>B/S Now</th>
                        <!-- Historical headers will be added dynamically -->
                    </tr>
                </thead>
                <tbody id="bs-tbody">
                    <!-- Table data will be populated dynamically -->
                </tbody>
            </table>
        </div>
        
        <div id="sb-tab" class="tab-content">
            <table id="sb-table">
                <thead>
                    <tr>
                        <th>Stock</th>
                        <th>LTP</th>
                        <th>Change %</th>
                        <th>Buy Qty</th>
                        <th>Sell Qty</th>
                        <th>S/B Now</th>
                        <!-- Historical headers will be added dynamically -->
                    </tr>
                </thead>
                <tbody id="sb-tbody">
                    <!-- Table data will be populated dynamically -->
                </tbody>
            </table>
        </div>
    </div>

    <script>
        // Global variables
        let marketData = [];
        let refreshIntervalId;
        let refreshRate = 1000; // Default to 1 second
        
        // Initialize the page
        document.addEventListener('DOMContentLoaded', function() {
            // Add historical headers to tables
            addHistoricalHeaders();
            
            // Initial data fetch
            fetchData();
            
            // Set up auto-refresh
            refreshIntervalId = setInterval(fetchData, refreshRate);
        });
        
        // Add historical headers to tables
        function addHistoricalHeaders() {
            const bsHeader = document.querySelector('#bs-table thead tr');
            const sbHeader = document.querySelector('#sb-table thead tr');
            
            // Intervals to display
            const intervals = [10, 20, 30, 40, 50, 60, 120, 240, 360, 480, 600];
            const intervalDisplay = intervals.map(i => i < 60 ? `${i}s` : `${i/60}m`);
            
            for (let i = 0; i < intervals.length; i++) {
                // Add headers to B/S table
                const bsTh = document.createElement('th');
                bsTh.textContent = 'B/S ' + intervalDisplay[i];
                bsHeader.appendChild(bsTh);
                
                // Add headers to S/B table
                const sbTh = document.createElement('th');
                sbTh.textContent = 'S/B ' + intervalDisplay[i];
                sbHeader.appendChild(sbTh);
            }
        }
        
        // Fetch data from API
        function fetchData() {
            fetch('/api/data')
                .then(response => response.json())
                .then(data => {
                    marketData = data.data;
                    document.getElementById('last-update').textContent = data.last_update;
                    document.getElementById('iteration').textContent = data.iteration;
                    
                    renderTables();
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        }
        
        // Render the tables with data
        function renderTables() {
            // Apply filters before rendering
            const filteredData = filterData();
            
            // Render the B/S table
            renderBSTable(filteredData);
            
            // Render the S/B table
            renderSBTable(filteredData);
        }
        
        // Filter data based on user inputs
        function filterData() {
            const minBSRatio = parseFloat(document.getElementById('min-bs-ratio').value) || 0;
            const minChange = parseFloat(document.getElementById('min-change').value) || -100;
            const searchStock = document.getElementById('search-stock').value.toUpperCase();
            
            return marketData.filter(stock => {
                const bsNumeric = typeof stock.bs_numeric === 'number' ? stock.bs_numeric : 0;
                const pctChange = typeof stock.pct_change === 'number' ? stock.pct_change : 0;
                
                return bsNumeric >= minBSRatio && 
                       pctChange >= minChange && 
                       stock.stock.includes(searchStock);
            });
        }
        
        // Apply filters and redraw tables
        function applyFilters() {
            renderTables();
        }
        
        // Render the B/S ratio table
        function renderBSTable(data) {
            const tbody = document.getElementById('bs-tbody');
            tbody.innerHTML = '';
            
            data.forEach(stock => {
                const row = document.createElement('tr');
                row.className = 'stock-row';
                
                // Basic stock info
                addCell(row, stock.stock);
                addCell(row, stock.ltp.toFixed(2));
                
                // Percent change with color
                const changeClass = stock.pct_change > 0 ? 'positive' : stock.pct_change < 0 ? 'negative' : 'neutral';
                const changeText = (stock.pct_change > 0 ? '+' : '') + stock.pct_change.toFixed(2) + '%';
                addCell(row, changeText, changeClass);
                
                // Quantities
                addCell(row, stock.buy_qty);
                addCell(row, stock.sell_qty);
                
                // Current B/S ratio with direction
                const bsClass = stock.bs_direction === '>' ? 'buy-dominant' : 
                               stock.bs_direction === '<' ? 'sell-dominant' : 'equal';
                addCell(row, `${stock.bs_ratio} ${stock.bs_direction}`, bsClass);
                
                // Historical B/S ratios
                const intervals = [10, 20, 30, 40, 50, 60, 120, 240, 360, 480, 600];
                intervals.forEach(interval => {
                    if (stock.historical_bs && stock.historical_bs[interval]) {
                        const [ratio, direction] = stock.historical_bs[interval];
                        const histClass = direction === '>' ? 'buy-dominant' : 
                                         direction === '<' ? 'sell-dominant' : 'equal';
                        addCell(row, `${ratio} ${direction}`, histClass);
                    } else {
                        addCell(row, 'N/A -');
                    }
                });
                
                tbody.appendChild(row);
            });
        }
        
        // Render the S/B ratio table
        function renderSBTable(data) {
            const tbody = document.getElementById('sb-tbody');
            tbody.innerHTML = '';
            
            data.forEach(stock => {
                const row = document.createElement('tr');
                row.className = 'stock-row';
                
                // Basic stock info
                addCell(row, stock.stock);
                addCell(row, stock.ltp.toFixed(2));
                
                // Percent change with color
                const changeClass = stock.pct_change > 0 ? 'positive' : stock.pct_change < 0 ? 'negative' : 'neutral';
                const changeText = (stock.pct_change > 0 ? '+' : '') + stock.pct_change.toFixed(2) + '%';
                addCell(row, changeText, changeClass);
                
                // Quantities
                addCell(row, stock.buy_qty);
                addCell(row, stock.sell_qty);
                
                // Current S/B ratio with direction
                const sbClass = stock.sb_direction === '>' ? 'sell-dominant' : 
                               stock.sb_direction === '<' ? 'buy-dominant' : 'equal';
                addCell(row, `${stock.sb_ratio} ${stock.sb_direction}`, sbClass);
                
                // Historical S/B ratios
                const intervals = [10, 20, 30, 40, 50, 60, 120, 240, 360, 480, 600];
                intervals.forEach(interval => {
                    if (stock.historical_sb && stock.historical_sb[interval]) {
                        const [ratio, direction] = stock.historical_sb[interval];
                        const histClass = direction === '>' ? 'sell-dominant' : 
                                         direction === '<' ? 'buy-dominant' : 'equal';
                        addCell(row, `${ratio} ${direction}`, histClass);
                    } else {
                        addCell(row, 'N/A -');
                    }
                });
                
                tbody.appendChild(row);
            });
        }
        
        // Helper function to add a cell to a row
        function addCell(row, content, className = '') {
            const cell = document.createElement('td');
            cell.innerHTML = content;
            if (className) {
                cell.className = className;
            }
            row.appendChild(cell);
        }
        
        // Switch between tabs
        function switchTab(tabId) {
            // Update tab buttons
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelector(`.tab[onclick="switchTab('${tabId}')"]`).classList.add('active');
            
            // Update tab content
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(tabId).classList.add('active');
        }
        
        // Update refresh interval
        function updateRefreshInterval() {
            refreshRate = parseInt(document.getElementById('refresh-interval').value);
            clearInterval(refreshIntervalId);
            refreshIntervalId = setInterval(fetchData, refreshRate);
        }
    </script>
</body>
</html>
    """)

# Initialize Flask app
app = Flask(__name__, static_folder=static_folder)

# Global variables to store data
latest_data = []
last_update_time = ""
iteration_count = 0

def calculate_ratios(buy_qty, sell_qty):
    """Calculate both B/S and S/B ratios and indicate direction."""
    # Calculate B/S ratio
    if sell_qty == 0:
        if buy_qty > 0:
            bs_ratio = float('inf')
            bs_ratio_str = "Inf"
            bs_direction = ">"
        else:
            bs_ratio = 0.0
            bs_ratio_str = "0.00"
            bs_direction = "="
    else:
        bs_ratio = buy_qty / sell_qty
        bs_ratio_str = f"{bs_ratio:.2f}"
        bs_direction = ">" if bs_ratio > 1 else "<" if bs_ratio < 1 else "="
    
    # Calculate S/B ratio
    if buy_qty == 0:
        if sell_qty > 0:
            sb_ratio = float('inf')
            sb_ratio_str = "Inf"
            sb_direction = ">"
        else:
            sb_ratio = 0.0
            sb_ratio_str = "0.00"
            sb_direction = "="
    else:
        sb_ratio = sell_qty / buy_qty
        sb_ratio_str = f"{sb_ratio:.2f}"
        sb_direction = ">" if sb_ratio > 1 else "<" if sb_ratio < 1 else "="
    
    return bs_ratio_str, bs_direction, bs_ratio, sb_ratio_str, sb_direction, sb_ratio

def get_historical_ratio(history_data, seconds, ratio_type='bs'):
    """Calculate the average ratio (B/S or S/B) over the specified time period."""
    if not history_data:
        return "N/A", "-"
    
    # Filter data points that are within the time window
    current_time = datetime.now().timestamp()
    window_data = [data for timestamp, data in history_data 
                  if current_time - timestamp <= seconds]
    
    if not window_data:
        return "N/A", "-"
    
    # Calculate average ratio (either B/S or S/B)
    ratio_key = 'bs_numeric' if ratio_type == 'bs' else 'sb_numeric'
    
    valid_values = [val for val in [data.get(ratio_key, None) for data in window_data] 
                   if val is not None and not isinstance(val, str) and 
                   not (val == float('inf') or val != val)]
    
    if not valid_values:
        return "N/A", "-"
    
    avg_ratio = sum(valid_values) / len(valid_values)
    direction = ">" if avg_ratio > 1 else "<" if avg_ratio < 1 else "="
    
    return f"{avg_ratio:.2f}", direction

def start_data_collection():
    """Start collecting market data in the background."""
    global latest_data, last_update_time, iteration_count
    
    try:
        # Initialize Tradehull client
        tsl = Tradehull(CLIENT_CODE, TOKEN_ID)
        
        # Create symbols map
        working_symbols = {stock: f"{stock} APR FUT" for stock in WATCHLIST}
        
        # Initialize historical data storage
        historical_data = defaultdict(lambda: deque(maxlen=max(HISTORY_INTERVALS) + 10))
        
        print(f"Starting futures monitoring for {len(WATCHLIST)} stocks...")
        
        # Monitor continuously
        iteration_count = 0
        while True:
            try:
                current_time = datetime.now().strftime("%H:%M:%S")
                timestamp = datetime.now().timestamp()
                stocks_data = []
                
                # Prepare all requests for batch processing
                symbols = list(working_symbols.values())
                
                # Get quote data in batch if possible
                try:
                    batch_quote_data = tsl.get_quote_data(names=symbols)
                except Exception as e:
                    print(f"Error getting quote data: {e}")
                    batch_quote_data = {}
                
                # Process data for each stock
                for stock, symbol in working_symbols.items():
                    try:
                        if batch_quote_data and symbol in batch_quote_data:
                            future_data = batch_quote_data[symbol]
                            
                            # Extract the data
                            ltp = future_data.get('last_price', 0)
                            prev_close = future_data.get('ohlc', {}).get('close', 0)
                            pct_change = ((ltp - prev_close) / prev_close * 100) if prev_close > 0 else 0
                            buy_qty = future_data.get('buy_quantity', 0)
                            sell_qty = future_data.get('sell_quantity', 0)
                            
                            # Calculate both ratios
                            bs_ratio, bs_direction, bs_numeric, sb_ratio, sb_direction, sb_numeric = calculate_ratios(buy_qty, sell_qty)
                            
                            # Store data for current iteration
                            stock_data = {
                                'stock': stock,
                                'ltp': ltp,
                                'pct_change': pct_change,
                                'buy_qty': buy_qty,
                                'sell_qty': sell_qty,
                                'bs_ratio': bs_ratio,
                                'bs_direction': bs_direction,
                                'bs_numeric': bs_numeric,
                                'sb_ratio': sb_ratio,
                                'sb_direction': sb_direction,
                                'sb_numeric': sb_numeric,
                                'timestamp': timestamp
                            }
                            
                            # Store in historical data
                            historical_data[stock].append((timestamp, stock_data))
                            
                            # Calculate historical ratios for both B/S and S/B
                            historical_bs = {}
                            historical_sb = {}
                            for interval in HISTORY_INTERVALS:
                                # B/S historical ratios
                                bs_avg_ratio, bs_direction = get_historical_ratio(
                                    [(ts, data) for ts, data in historical_data[stock]], 
                                    interval, 'bs'
                                )
                                historical_bs[interval] = (bs_avg_ratio, bs_direction)
                                
                                # S/B historical ratios
                                sb_avg_ratio, sb_direction = get_historical_ratio(
                                    [(ts, data) for ts, data in historical_data[stock]], 
                                    interval, 'sb'
                                )
                                historical_sb[interval] = (sb_avg_ratio, sb_direction)
                            
                            # Add historical data to the stock data
                            stock_data['historical_bs'] = historical_bs
                            stock_data['historical_sb'] = historical_sb
                            
                            # Store the data for display
                            stocks_data.append(stock_data)
                    except Exception as e:
                        print(f"Error processing {stock}: {e}")
                        continue
                
                # Skip update if no data
                if not stocks_data:
                    time.sleep(0.5)
                    continue
                
                # Sort stocks by BS ratio (highest to lowest)
                stocks_data.sort(key=lambda x: x['bs_numeric'] if isinstance(x['bs_numeric'], (int, float)) 
                               and x['bs_numeric'] != float('inf') else 0, reverse=True)
                
                # Update global data
                latest_data = stocks_data
                last_update_time = current_time
                iteration_count += 1
                
                # Print update info to console
                if iteration_count % 5 == 0:  # Print less frequently to reduce console spam
                    print(f"Updated at {current_time} | Iteration: {iteration_count} | Stocks: {len(stocks_data)}")
                
                # Wait before the next update
                time.sleep(UPDATE_INTERVAL)
                
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(1)
    
    except Exception as e:
        print(f"Critical error in data collection: {e}")

@app.route('/', methods=['GET'])
def index():
    """Serve the main HTML page."""
    try:
        print("Serving index.html")
        return app.send_static_file('index.html')
    except Exception as e:
        print(f"Error serving index.html: {e}")
        return f"Error loading dashboard. Check server logs. Error: {str(e)}", 500

@app.route('/test')
def test_page():
    """A simple test page to check if the server is working."""
    return "Server is working! Go to the <a href='/'>Dashboard</a>"

@app.route('/api/data')
def get_data():
    """API endpoint to fetch the latest data."""
    global latest_data, last_update_time, iteration_count
    
    try:
        # Create a response with all the necessary data
        response = {
            'data': latest_data,
            'last_update': last_update_time,
            'iteration': iteration_count,
            'intervals': HISTORY_INTERVALS
        }
        
        return jsonify(response)
    except Exception as e:
        print(f"Error in API: {e}")
        return jsonify({
            'error': str(e),
            'data': [],
            'last_update': datetime.now().strftime("%H:%M:%S"),
            'iteration': iteration_count,
            'intervals': HISTORY_INTERVALS
        })

def main():
    """Main entry point for the application."""
    import threading
    
    # Start data collection in a separate thread
    data_thread = threading.Thread(target=start_data_collection)
    data_thread.daemon = True  # This ensures the thread will exit when the main program exits
    data_thread.start()
    
    # Start the Flask web server
    print("Starting web server on http://localhost:5000")
    print("You can also try http://127.0.0.1:5000 or http://[your-ip-address]:5000")
    print("A test page is available at http://localhost:5000/test")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

if __name__ == "__main__":
    main()