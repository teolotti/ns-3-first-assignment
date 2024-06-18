import xml.etree.ElementTree as ET
import pandas as pd

def parse_flow_monitor_to_table(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    data = []
    
    for flow in root.findall(".//FlowStats"):
        flow_id = flow.attrib['flowId']
        tx_packets = int(flow.attrib['txPackets'])
        rx_packets = int(flow.attrib['rxPackets'])
        lost_packets = tx_packets - rx_packets
        delay_sum = float(flow.attrib['delaySum'].split(' ')[0])
        tx_bytes = int(flow.attrib['txBytes'])
        rx_bytes = int(flow.attrib['rxBytes'])
        time_first_tx_packet = float(flow.attrib['timeFirstTxPacket'].split(' ')[0])
        time_last_rx_packet = float(flow.attrib['timeLastRxPacket'].split(' ')[0])
        duration = time_last_rx_packet - time_first_tx_packet
        
        rtt = delay_sum / rx_packets if rx_packets > 0 else 0
        throughput = (rx_bytes * 8) / duration if duration > 0 else 0

        data.append({
            "Flow ID": flow_id,
            "Tx Packets": tx_packets,
            "Rx Packets": rx_packets,
            "Lost Packets": lost_packets,
            "RTT (s)": rtt,
            "Throughput (bps)": throughput
        })

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = parse_flow_monitor_to_table("scratch/first/first-ass-tcp.xml")
    print(df)
    df.to_csv("flow_monitor_results.csv", index=False)
