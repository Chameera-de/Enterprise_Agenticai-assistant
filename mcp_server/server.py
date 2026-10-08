"""Enterprise MCP server. Run: python -m mcp_server.server (requires `mcp`)."""
DATA={
 'employees': {'E1001':{'name':'N. Perera','department':'Payments','title':'SRE Lead'}},
 'services': {'payment-api':{'owner':'Payments','tier':'critical','status':'operational'}},
 'incidents': {'INC-2025-017':{'service':'payment-api','severity':'SEV1','root_cause':'connection pool exhaustion'}}
}
try:
    from mcp.server.fastmcp import FastMCP
    mcp=FastMCP('enterprise-data')
    @mcp.tool()
    def employee_lookup(employee_id:str): return DATA['employees'].get(employee_id,{'error':'not found'})
    @mcp.tool()
    def service_lookup(service_name:str): return DATA['services'].get(service_name,{'error':'not found'})
    @mcp.tool()
    def incident_lookup(incident_id:str): return DATA['incidents'].get(incident_id,{'error':'not found'})
except Exception:
    mcp=None

if __name__=='__main__':
    if mcp is None: raise SystemExit('Install the mcp package to run the MCP server')
    mcp.run()
