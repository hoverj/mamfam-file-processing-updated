SHIP_TO_HOME_TABLE_START = """   
<div id="table-section">
        <div class="table-name">Ship to Home</div>
        <table>
            <thead>
                <tr>
                    <th>Customer Name</th>
                    <th>Product Ordered</th>
                    <th>Quantity</th>
                    <th>Total Collected</th>
                    <th>Customization</th>
                </tr>
            </thead>
            <tbody>
"""
SHIP_TO_ORG_TABLE_START = """
    <div id="table-section">
        <div class="table-name">Ship to Organization</div>
        <table>
            <thead>
                <tr>
                    <th>Customer Name</th>
                    <th>Product Ordered</th>
                    <th>Quantity</th>
                    <th>Total Collected</th>
                    <th>Customization</th>
                </tr>
            </thead>
            <tbody>
"""
BROCHURE_TABLE_START = """    
    <div id="table-section">
        <div class="table-name">Brochure Sales</div>
        <table>
            <thead>
                <tr>
                    <th>Product Ordered</th>
                    <th>Quantity</th>
                    <th>Total Collected</th>
                </tr>
            </thead>
            <tbody>
"""
STUDENT_QUICK_TABLE_HEADER = """
<table>
      <thead>
          <tr>
              <th>Item</th>
              <th>Quantity</th>
              <th>Total Collected</th>
          </tr>
      </thead>
      <tbody>
"""
PARTICIPANT_TOTAL_TABLE = """    
    <div id="table-section">
        <div class="table-name">Totals</div>
        <table>
            <thead>
                <tr>
                    <th> </th>
                    <th># Items Sold</th>
                    <th>$ Amount Sold</th>
                </tr>
            </thead>
            <tbody>
    """
PARTICIPANT_DETAILED_TOTAL_TABLE_START = """

    <div id="table-section">
        <div class="table-name">Totals</div>
        <table>
            <thead>
                <tr>
                    <th> </th>
                    <th># Items Sold</th>
                    <th>$ Amount Sold</th>
                </tr>
            </thead>
            <tbody>
"""
PARTICIPANT_QUICK_TABLE_START = """
    <table>
      <thead>
          <tr>
              <th>Item</th>
              <th>Quantity</th>
              <th>Total Collected</th>
          </tr>
      </thead>
      <tbody>
    """
ORG_PARTICIPANT_WRITEUP_START = """
        <table>
            <thead>
                <tr>
                    <th>Primary Div</th>
                    <th>Secondary Div</th>
                    <th>Participant</th>
                    <th>S2H Items</th>
                    <th>S2H Money</th>
                    <th>S2O Items</th>
                    <th>S2O Money</th>
                    <th>Broch Items</th>
                    <th>Broch Money</th>
                    <th>Total Items</th>
                    <th>Total Money</th>
                    <th>Total Profit</th>
                </tr>
            </thead>
            <tbody>
"""
HTML_BOILER_PLATE_START = """
<html>
<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link rel="stylesheet" type="text/css" href="../../../../../src/html_generation/file_generation.css">
</head>

<body>
    """
HTML_BOILER_PLATE_ORG_LEVEL_START = """
<html>
<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link rel="stylesheet" type="text/css" href="../../../src/html_generation/file_generation.css">
</head>

<body>
    """
ORG_ITEMS_SOLD_TABLE_START = """
        <table>
            <thead>
                <tr>
                    <th>Item Name</th>
                    <th>S2O Items</th>
                    <th>S2H Items</th>
                    <th>Brochure Items</th>
                    <th>Total Items</th>
                </tr>
            </thead>
            <tbody>
"""
HTML_END = """
    </body>
    </html>
"""
END_TABLE = """
            </tbody>
        </table>
    </div>
"""
