import boto.ec2

def main():
	# create connection
	conn = boto.ec2.connect_to_region("us-east-1", aws_access_key_id='XXXX', aws_secret_access_key = 'XXXX')
	
	# create and save key-pair
	key_pair = conn.create_key_pair("csc326-group32-key-pair")
	key_pair.save("/Users/hhaider/Desktop/CSC326/python-search-engine/lab2/")

	# create and authorize security group
	group = conn.create_security_group("csc326-group32", "csc326-group32-security-group")
	group.authorize('icmp', -1, -1, '0.0.0.0/0')
	group.authorize('tcp', 22, 22, '0.0.0.0/0')
	group.authorize('tcp', 80, 80, '0.0.0.0/0')

	# run instance, this created instance "i-8bff176a"
	reservation = conn.run_instances('ami-8caa1ce4', instance_type='t1.micro' key_name='csc326-group32-key-pair', security_groups=['csc326-group32'])
	
	# elastic ip for "i-8bff176a"
	address = conn.allocate_address()
	address.associate("i-8bff176a")

if __name__ == "__main__":
	main()