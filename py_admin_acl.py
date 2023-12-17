from kafka.admin import KafkaAdminClient, ACLPermissionType, ResourcePattern, ResourceType, ACL, ACLOperation, ACLFilter

brokers = 'localhost:9092'

admin = KafkaAdminClient(
    bootstrap_servers=brokers,
    security_protocol='SASL_PLAINTEXT',
    sasl_mechanism='PLAIN',
    sasl_plain_username='admin',      # your privileged user
    sasl_plain_password='admin-secret'  # password
)


acl1 = ACL(
    principal="User:user1",
    host="*",
    operation=ACLOperation.READ,
    permission_type=ACLPermissionType.ALLOW,
    resource_pattern=ResourcePattern(ResourceType.TOPIC, 'topic2')
)
acl2 = ACL(
    principal="User:user1",
    host="*",
    operation=ACLOperation.READ,
    permission_type=ACLPermissionType.ALLOW,
    resource_pattern=ResourcePattern(ResourceType.GROUP, 'group2')
)
acl3 = ACL(
    principal="User:user2",
    host="*",
    operation=ACLOperation.WRITE,
    permission_type=ACLPermissionType.ALLOW,
    resource_pattern=ResourcePattern(ResourceType.TOPIC, 'topic2')
)


acls_result = admin.create_acls([acl1, acl2, acl3])
print(acls_result)