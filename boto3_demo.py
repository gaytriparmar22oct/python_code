"""
boto3 — the AWS SDK for Python (automate anything in AWS).

Why SREs care: boto3 is how you script AWS — list/stop EC2, read/write S3,
push CloudWatch metrics, manage IAM. Nearly every AWS-focused SRE role expects
familiarity with it.

Install once:  pip install boto3
Run:           python boto3_demo.py   (needs AWS credentials configured)

This demo is READ-ONLY and degrades gracefully: if boto3 isn't installed or no
credentials/region are set, it prints a message instead of crashing.
"""


def main():
    try:
        import boto3
        from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError
    except ImportError:
        print("boto3 not installed. Run: pip install boto3")
        return

    # -----------------------------------------------------------------------
    # 1. A "client" is a low-level 1:1 mapping to an AWS service's API.
    #    boto3 finds credentials automatically (env vars, ~/.aws/credentials,
    #    IAM role on EC2/EKS, SSO) — the "credential provider chain".
    # -----------------------------------------------------------------------
    try:
        ec2 = boto3.client("ec2", region_name="eu-west-1")

        # 2. Describe EC2 instances (like `aws ec2 describe-instances`).
        print("--- EC2 instances (eu-west-1) ---")
        reservations = ec2.describe_instances().get("Reservations", [])
        found = False
        for res in reservations:
            for inst in res["Instances"]:
                found = True
                print(f"{inst['InstanceId']}  {inst['InstanceType']}  "
                      f"{inst['State']['Name']}")
        if not found:
            print("(no instances)")

        # 3. Another service: list S3 buckets (global).
        s3 = boto3.client("s3")
        print("\n--- S3 buckets ---")
        for b in s3.list_buckets().get("Buckets", []):
            print(b["Name"])

        # 4. Push a custom CloudWatch metric (commented — it WRITES data).
        # cw = boto3.client("cloudwatch", region_name="eu-west-1")
        # cw.put_metric_data(
        #     Namespace="MyApp",
        #     MetricData=[{"MetricName": "HealthyHosts", "Value": 3}],
        # )

    except NoCredentialsError:
        print("No AWS credentials found. Configure with `aws configure`.")
    except (ClientError, BotoCoreError) as e:
        print(f"AWS call failed (likely no creds/permissions): {e}")


if __name__ == "__main__":
    main()
