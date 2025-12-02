# AWS Architecture

## Why ECS over EKS

I chose ECS Fargate for this deployment:

- MyCandidate is a single Flask app, not microservices - EKS is overkill
- ECS has no control plane cost (EKS charges $73/month just for the cluster)
- Simpler to manage for a small team
- Still provides auto-scaling and high availability

## Components

**Compute:** ECS Fargate
- 2 tasks minimum, scales to 10 during elections
- 0.5 vCPU, 1GB memory per task
- Runs our Docker container

**Database:** RDS PostgreSQL
- db.t3.small instance
- Multi-AZ for failover
- Automated backups

**Cache:** ElastiCache Redis
- cache.t3.micro
- Handles session data and API caching

**Load Balancing:** Application Load Balancer
- Distributes traffic across tasks
- SSL termination
- Health checks

**Networking:** VPC with public/private subnets
- ALB in public subnet
- ECS tasks and database in private subnets
- NAT Gateway for outbound traffic

**Secrets:** AWS Secrets Manager
- Database credentials
- Flask SECRET_KEY

## Security

- All app components in private subnets (no public IPs)
- Security groups restrict traffic between components
- HTTPS only via ALB
- Database encrypted at rest
- Non-root container user (from our Dockerfile)

## Scaling

Auto-scaling based on CPU:
- Scale out when CPU > 70%
- Scale in when CPU < 30%
- Min 2 tasks, max 10 tasks

Election periods see traffic spikes. The architecture handles this by:
1. Auto-scaling ECS tasks based on load
2. Redis caching reduces database hits
3. CloudFront can cache static assets

## Instance Sizing

| Component | Size | Why |
|-----------|------|-----|
| ECS Tasks | 0.5 vCPU, 1GB | Flask app is lightweight |
| RDS | db.t3.small | Handles typical load, can scale up |
| ElastiCache | cache.t3.micro | Caching doesn't need much |

## Cost Estimate

Monthly (normal traffic):
- ECS Fargate (2 tasks): ~$30
- RDS Multi-AZ: ~$50
- ElastiCache: ~$12
- ALB: ~$20
- NAT Gateway: ~$35
- Other (S3, Secrets): ~$5
- **Total: ~$150/month**

During elections (scaled up): ~$220/month
