"""Create the explicit computational benchmark protocol."""
from ceh.protocol import write_protocol

if __name__=="__main__":
    protocol,path=write_protocol()
    print(f"wrote {path}")
    print(protocol)
