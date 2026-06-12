"""
Gradio Frontend for Multi-Agent Deal Discovery System
"""
import gradio as gr
from deal_agent_framework import DealAgentFramework

# Global framework instance
framework = None


def initialize_system():
    """Initialize the framework"""
    global framework
    try:
        if framework is None:
            framework = DealAgentFramework()
        return "System initialized - Using Ollama Gemma 2B"
    except Exception as e:
        return f"Error initializing: {str(e)}"


def run_deal_discovery():
    """Run the deal discovery workflow"""
    global framework
    
    if framework is None:
        try:
            framework = DealAgentFramework()
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            error_msg = f"""
### Initialization Error

**Error:** {str(e)}

**Details:**
```
{error_detail}
```

**Note:** This system runs locally with Ollama

**Check:**
1. Ollama is running: `ollama serve`
2. Gemma 2B model exists: `ollama list | grep gemma:2b`
3. If missing, pull it: `ollama pull gemma:2b`
"""
            return error_msg, [], f"Init Error: {str(e)[:50]}"
    
    try:
        # Run the discovery
        opportunities = framework.run()
        
        if not opportunities:
            return """
### No New Deals Found

The RSS feeds may be:
- Empty at the moment
- Already fully scraped
- Temporarily unavailable

**Try again later or the system has already found all current deals!**

Check memory.json file to see previously found deals.
""", [], "No new deals - check again later"
        
        # Get the latest opportunity
        latest = opportunities[-1]
        
        # Format summary
        summary = f"""
### Latest Deal Found!

**Discount:** ${latest.discount:.2f}  
**Price:** ${latest.deal.price:.2f}  
**Estimated Value:** ${latest.estimate:.2f}  
**Savings:** {(latest.discount/latest.estimate*100):.1f}%

---

**Product:**  
{latest.deal.product_description}

---

**URL:** [{latest.deal.url}]({latest.deal.url})

---

*Priced using Gemma 2B (local Ollama)*
"""
        
        # Format all opportunities table
        table_data = []
        for i, opp in enumerate(opportunities[-10:], 1):
            table_data.append([
                i,
                f"${opp.discount:.2f}",
                f"${opp.deal.price:.2f}",
                f"${opp.estimate:.2f}",
                opp.deal.product_description[:60] + "..."
            ])
        
        return summary, table_data, f"Success: {len(opportunities)} total"
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        error_msg = f"""
### Runtime Error

**Error:** {str(e)}

**Full Traceback:**
```
{error_detail}
```

**Common Issues:**
- **Ollama not running:** Run `ollama serve` in terminal
- **Missing model:** Run `ollama pull gemma:2b`
- **Network issues:** Check internet connection for RSS feeds
"""
        return error_msg, [], f"Error: {str(e)[:100]}"


def view_all_opportunities():
    """View all saved opportunities"""
    global framework
    
    if framework is None:
        framework = DealAgentFramework()
    
    if not framework.memory:
        return [], "No opportunities in memory yet. Run 'Deal Discovery' first!"
    
    table_data = []
    for i, opp in enumerate(framework.memory, 1):
        table_data.append([
            i,
            f"${opp.discount:.2f}",
            f"${opp.deal.price:.2f}",
            f"${opp.estimate:.2f}",
            f"{(opp.discount/opp.estimate*100):.1f}%",
            opp.deal.product_description[:60] + "...",
            opp.deal.url
        ])
    
    return table_data, f"Total: {len(framework.memory)} opportunities found"


def clear_memory():
    """Clear all opportunities from memory"""
    global framework
    
    if framework is None:
        framework = DealAgentFramework()
    
    framework.memory = []
    framework._save_memory()
    
    return [], "Memory cleared - ready for fresh deals!"


# Create Gradio Interface
with gr.Blocks(title="Deal Discovery System", theme=gr.themes.Soft()) as demo:
    
    gr.Markdown("""
    # Multi-Agent Deal Discovery System
    
    Local AI-powered system using Ollama with Gemma 2B
    
    - **Scanner Agent**: Finds deals from RSS feeds
    - **Specialist Agent**: Estimates fair prices using Gemma 2B
    - **Planning Agent**: Identifies great bargains
    
    ---
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### Control Panel")
            
            init_btn = gr.Button("Initialize System", variant="secondary", size="sm")
            init_status = gr.Textbox(label="Status", interactive=False, lines=2)
            
            gr.Markdown("---")
            
            discover_btn = gr.Button("Run Deal Discovery", variant="primary", size="lg")
            status_text = gr.Textbox(label="Discovery Status", interactive=False, lines=2)
            
        with gr.Column(scale=3):
            gr.Markdown("### Latest Deal")
            latest_deal = gr.Markdown("Click 'Run Deal Discovery' to find deals...")
    
    gr.Markdown("---")
    
    with gr.Row():
        gr.Markdown("### Recent Opportunities (Last 10)")
    
    recent_table = gr.Dataframe(
        headers=["#", "Discount", "Price", "Estimate", "Product"],
        datatype=["number", "str", "str", "str", "str"],
        interactive=False,
        wrap=True
    )
    
    gr.Markdown("---")
    
    with gr.Accordion("All Opportunities", open=False):
        with gr.Row():
            view_all_btn = gr.Button("View All", variant="secondary")
            clear_btn = gr.Button("Clear Memory", variant="stop")
        
        all_status = gr.Textbox(label="Status", interactive=False, lines=1)
        
        all_table = gr.Dataframe(
            headers=["#", "Discount", "Price", "Estimate", "Savings %", "Product", "URL"],
            datatype=["number", "str", "str", "str", "str", "str", "str"],
            interactive=False,
            wrap=True
        )
    
    gr.Markdown("""
    ---
    
    ### Tips
    - **First time?** Click "Initialize System" to set up
    - **Find deals:** Click "Run Deal Discovery" to scan RSS feeds  
    - **Local AI:** Uses Ollama with Gemma 2B model
    
    ### Requirements
    - Ollama running: `ollama serve`
    - Gemma 2B model: `ollama pull gemma:2b`
    """)
    
    # Connect buttons to functions
    init_btn.click(
        fn=initialize_system,
        outputs=init_status
    )
    
    discover_btn.click(
        fn=run_deal_discovery,
        outputs=[latest_deal, recent_table, status_text]
    )
    
    view_all_btn.click(
        fn=view_all_opportunities,
        outputs=[all_table, all_status]
    )
    
    clear_btn.click(
        fn=clear_memory,
        outputs=[all_table, all_status]
    )


if __name__ == "__main__":
    print("Starting Deal Discovery System with Ollama...")
    print("Open your browser at: http://localhost:7861")
    demo.launch(server_name="127.0.0.1", server_port=7861, share=False)
