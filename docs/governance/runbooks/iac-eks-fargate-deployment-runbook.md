# Runbook: AWS EKS Fargate Deployment & Cluster Synchronization

> **Document Type:** Runbook  
> **Status:** Ratified  
> **Governing Standards:** `CR-IAC-001`, `CR-BAI-001`, `CR-CICCCDCT-001`  
> **Target Subsystems:** AWS EKS Clusters, Kubernetes Deployments  
> **Tracking Issues:** Bayly-AI/HATH0R-Agentic-Framework#260, Bayly-AI/HATH0R-CLI#441

---

## 1. Scope & Objective

Operational runbook for provisioning AWS EKS Fargate profiles, validating IAM execution roles, and deploying cryptographically salted container workloads across canonical environments (`development`, `testing`, `staging`, `master`).

---

## 2. Infrastructure Pre-requisites

- **EKS Cluster**: Running Kubernetes >= 1.28.
- **VPC Subnets**: Minimum 2 private subnets tagged with `kubernetes.io/role/internal-elb: 1`.
- **Pod Execution Role**: IAM Role with AWS managed policy `AmazonEKSFargatePodExecutionRolePolicy`.
- **AWS Load Balancer Controller**: Deployed in `kube-system` to provision ALBs for IP target type ingresses.

---

## 3. Deployment Procedure

### Step 1: Render Environment Manifests
Render the manifests for the target promotion stage:

```bash
hath0r iac render . --env <development|testing|staging|master>
```

The rendered manifests are placed in `build/iac/<env>/`.

### Step 2: Apply AWS EKS Fargate Profile
Ensure the Fargate profile exists in the target cluster:

```bash
aws eks create-fargate-profile \
  --cluster-name hath0r-eks-cluster \
  --fargate-profile-name <app-name>-profile \
  --pod-execution-role-arn arn:aws:iam::<account>:role/AmazonEKSFargatePodExecutionRole \
  --selectors namespace=<app-namespace>
```

Wait for profile status to become `ACTIVE`:

```bash
aws eks wait fargate-profile-active \
  --cluster-name hath0r-eks-cluster \
  --fargate-profile-name <app-name>-profile
```

### Step 3: Deploy Salted Manifests
Apply the rendered Kubernetes manifests:

```bash
kubectl apply -f build/iac/<env>/ -n <app-namespace>
```

### Step 4: Verify Fargate Pod Scheduling
Check that pods are scheduled onto Fargate microVMs:

```bash
kubectl get pods -n <app-namespace> -o wide
```

*Note:* Fargate node names follow the pattern `fargate-ip-x-x-x-x...`.

### Step 5: ALB Healthcheck Verification
Verify ingress address and DNS propagation:

```bash
kubectl get ingress -n <app-namespace>
```

Inspect target group health:

```bash
aws elbv2 describe-target-health --target-group-arn <target-group-arn>
```

---

## 4. Troubleshooting & Remediation

| Symptom | Root Cause | Remediation |
| :--- | :--- | :--- |
| `Pod stuck in Pending` | No matching Fargate profile selector or subnets missing | Ensure namespace and labels match `fargate-profile.yaml` selectors. Check private subnet tags. |
| `ErrImagePull / ImagePullBackOff` | Pod Execution Role lacks ECR pull permissions | Attach `AmazonEC2ContainerRegistryReadOnly` policy to Fargate Pod Execution Role. |
| `CrashLoopBackOff` | Application wrote to read-only root disk | Mount an `emptyDir` volume at `/tmp` or the target writable path. |
| `ALB Ingress 502 Bad Gateway` | Target type not set to `ip` | Ensure `alb.ingress.kubernetes.io/target-type: ip` annotation is present. NodePort mode fails on Fargate. |
