#!/usr/bin/env bash
# Deploy OIDC provider and IAM role for AWS News Summary CI/CD.
#
# Usage:
#   # GitHub Actions (role: GitHubActions-AWSNewsSummary, stack: awsnews-summary-github-iam)
#   ./scripts/deploy-iam.sh -p github -o myorg -r awsnews-summary
#
#   # GitLab CI (role: GitLabCI-AWSNewsSummary, stack: awsnews-summary-gitlab-iam)
#   ./scripts/deploy-iam.sh -p gitlab -g mygroup -r awsnews-summary
#
#   # Custom role name and region
#   ./scripts/deploy-iam.sh -p github -o myorg -r awsnews-summary -n MyRole -R us-west-2

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STACK_NAME=""
REGION="us-east-1"
ROLE_NAME=""
PLATFORM=""
ORG_OR_GROUP=""
REPO_OR_PROJECT=""

usage() {
  cat <<EOF
Usage: $0 -p PLATFORM [OPTIONS]

Required:
  -p, --platform PLATFORM   github or gitlab

Platform-specific:
  GitHub:
    -o, --org ORG             GitHub owner/org
    -r, --repo REPO           GitHub repository name

  GitLab:
    -g, --group GROUP         GitLab group/namespace
    -r, --repo REPO           GitLab project name

Optional:
  -n, --role-name NAME        IAM role name (default: GitHubActions-AWSNewsSummary or GitLabCI-AWSNewsSummary)
  -s, --stack-name NAME       CloudFormation stack name (default: awsnews-summary-github-iam or awsnews-summary-gitlab-iam)
  -R, --region REGION         AWS region (default: us-east-1)
  -h, --help                  Show this help
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -p|--platform)   PLATFORM="$2"; shift 2 ;;
    -o|--org)        ORG_OR_GROUP="$2"; shift 2 ;;
    -g|--group)      ORG_OR_GROUP="$2"; shift 2 ;;
    -r|--repo)       REPO_OR_PROJECT="$2"; shift 2 ;;
    -n|--role-name)  ROLE_NAME="$2"; shift 2 ;;
    -s|--stack-name) STACK_NAME="$2"; shift 2 ;;
    -R|--region)     REGION="$2"; shift 2 ;;
    -h|--help)       usage ;;
    *)               echo "Error: Unknown option: $1"; usage ;;
  esac
done

# Validate
if [[ -z "$PLATFORM" ]]; then
  echo "Error: -p/--platform is required (github or gitlab)."
  usage
fi

if [[ "$PLATFORM" != "github" && "$PLATFORM" != "gitlab" ]]; then
  echo "Error: platform must be 'github' or 'gitlab'."
  usage
fi

if [[ -z "$ORG_OR_GROUP" ]]; then
  if [[ "$PLATFORM" == "github" ]]; then
    echo "Error: -o/--org is required for GitHub."
  else
    echo "Error: -g/--group is required for GitLab."
  fi
  usage
fi

if [[ -z "$REPO_OR_PROJECT" ]]; then
  echo "Error: -r/--repo is required."
  usage
fi

# Select template and parameters
if [[ "$PLATFORM" == "github" ]]; then
  [[ -z "$ROLE_NAME" ]] && ROLE_NAME="GitHubActions-AWSNewsSummary"
  [[ -z "$STACK_NAME" ]] && STACK_NAME="awsnews-summary-github-iam"
  TEMPLATE="${SCRIPT_DIR}/cfn-github-oidc-iam.yaml"
  PARAMS="RoleName=${ROLE_NAME} GitHubOrg=${ORG_OR_GROUP} GitHubRepo=${REPO_OR_PROJECT}"
  LABEL="GitHub Actions"
  REPO_DISPLAY="${ORG_OR_GROUP}/${REPO_OR_PROJECT}"
else
  [[ -z "$ROLE_NAME" ]] && ROLE_NAME="GitLabCI-AWSNewsSummary"
  [[ -z "$STACK_NAME" ]] && STACK_NAME="awsnews-summary-gitlab-iam"
  TEMPLATE="${SCRIPT_DIR}/cfn-gitlab-oidc-iam.yaml"
  PARAMS="RoleName=${ROLE_NAME} GitLabGroup=${ORG_OR_GROUP} GitLabProject=${REPO_OR_PROJECT}"
  LABEL="GitLab CI"
  REPO_DISPLAY="${ORG_OR_GROUP}/${REPO_OR_PROJECT}"
fi

echo "=== AWS News Summary IAM Setup ==="
echo "Platform: ${LABEL}"
echo "Repo:     ${REPO_DISPLAY}"
echo "Stack:    ${STACK_NAME}"
echo "Region:   ${REGION}"
echo "Role:     ${ROLE_NAME}"
echo ""

export AWS_PAGER=""

echo "Deploying CloudFormation stack..."
aws cloudformation deploy \
  --template-file "$TEMPLATE" \
  --stack-name "$STACK_NAME" \
  --region "$REGION" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides $PARAMS

echo ""
echo "=== Stack Outputs ==="
aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --region "$REGION" \
  --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
  --output table

echo ""
echo "Done. Set the RoleArn above as AWS_ROLE_ARN in your ${LABEL} variables."
