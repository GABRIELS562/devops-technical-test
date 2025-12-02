# Generate AWS architecture diagram
# Run: pip install diagrams && python architecture_diagram.py

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Fargate
from diagrams.aws.database import RDS, ElastiCache
from diagrams.aws.network import ALB, NATGateway, InternetGateway
from diagrams.aws.security import SecretsManager
from diagrams.aws.general import Users

graph_attr = {
    "fontsize": "20",
    "bgcolor": "white",
    "pad": "0.5"
}

with Diagram(
    "MyCandidate AWS Architecture",
    show=False,
    filename="architecture",
    direction="LR",
    graph_attr=graph_attr
):

    users = Users("Users")

    with Cluster("VPC (af-south-1)"):

        igw = InternetGateway("Internet\nGateway")

        with Cluster("Public Subnet"):
            alb = ALB("Application\nLoad Balancer")
            nat = NATGateway("NAT Gateway")

        with Cluster("Private Subnet"):

            with Cluster("ECS Fargate\n(min 2, max 10 tasks)"):
                task1 = Fargate("Task")
                task2 = Fargate("Task")

            with Cluster("Data Layer"):
                rds = RDS("PostgreSQL\ndb.t3.small\n(Multi-AZ)")
                redis = ElastiCache("Redis\ncache.t3.micro")

            secrets = SecretsManager("Secrets\nManager")

    # User traffic flow
    users >> Edge(label="HTTPS", color="darkgreen") >> igw
    igw >> Edge(label="Port 443") >> alb

    # ALB distributes to ECS tasks
    alb >> Edge(label="Traffic", color="orange") >> task1
    alb >> Edge(label="Traffic", color="orange") >> task2

    # ECS to database
    task1 >> Edge(label="SQL", color="blue") >> rds
    task2 >> Edge(label="SQL", color="blue") >> rds

    # ECS to cache
    task1 >> Edge(label="Cache", color="purple", style="dashed") >> redis
    task2 >> Edge(label="Cache", color="purple", style="dashed") >> redis

    # Secrets access (DB creds, Flask SECRET_KEY)
    task1 >> Edge(label="Creds", color="red", style="dotted") >> secrets

    # Outbound internet via NAT
    task1 >> Edge(label="Outbound", style="dashed", color="gray") >> nat
