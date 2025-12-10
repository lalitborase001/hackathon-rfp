from sales_agent import SalesAgent

def test_list_available_rfps():
    sales_agent = SalesAgent()
    available_rfps = sales_agent.list_available_rfps()
    print(available_rfps)

def test_summarize_rfp():
    sales_agent = SalesAgent()
    file_path = 'data/rfps/rfp1.txt'
    rfp_info = sales_agent.summarize_rfp(file_path)
    print(rfp_info)

if __name__ == '__main__':
    test_list_available_rfps()
    test_summarize_rfp()
