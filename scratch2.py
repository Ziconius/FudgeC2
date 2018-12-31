import scratch

x = scratch.ImplantSingleton

print(x.instance)
print(x.instance.UID)

y = scratch.ImplantSingleton.instance
print(y.UID)

y.AddCommand("Whoami")
print(y.IssueCommand())