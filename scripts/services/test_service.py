from discovery_service import DiscoveryService


service = DiscoveryService()

print()

print("New")
print(len(service.new_pages()))

print()

print("Events")
print(len(service.events()))

print()

print("High Priority")
print(len(service.high_priority()))