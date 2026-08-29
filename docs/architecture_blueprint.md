# Cloud, Security & IoT Deployment Blueprint

## Task 9: Distributed Architecture & Communication Plan
We select a **Hybrid** architecture combining edge autonomous processing across the three zone controllers with a central Smart City Operations dashboard.
* **Transparency**: The dashboard maintains a unified real-time topology view of all three zone controllers.
* **Fault Tolerance**: If the central dashboard fails, local zone controllers continue executing the *scheduler and Banker's Algorithm engine from Part 1* autonomously.
* **Scalability**: Heavy job execution resides within regional zone clusters without overloading central ingress.

### Data Flow Protocol Specifications:
a) **Zone controller pushing a real-time public-safety alert**: **Asynchronous** flow using **MQTT** over TLS (QoS 1). Emergency events must bypass synchronous HTTP head-of-line blocking for instant transmission.
b) **Zone controller uploading daily sensor logs**: **Synchronous** flow using **HTTP/HTTPS** POST requests. Requires request-response transport layer verification to ensure chunked archival integrity.

---

## Task 10: VPC-Based Network Boundary
We deploy **3 Subnets within 1 single VPC**:
* `Zone-A Subnet` (`10.0.1.0/24`)
* `Zone-B Subnet` (`10.0.2.0/24`)
* `Zone-C Subnet` (`10.0.3.0/24`)

### Isolation Control:
Cross-zone communication is strictly restricted using explicit **Network Access Control Lists (NACLs)** applied at subnet boundaries, blocking traffic from `10.0.2.0/24` directly targeting `10.0.1.0/24`. All zone updates route through private interface endpoints feeding the central dashboard API.

---

## Task 11: Network Security Objectives Mapping
1. **Protect Sensitive Data**: Encrypt data in transit with TLS 1.3 and at rest with AWS KMS / AES-256 keys.
2. **Authentication**: Enforce OAuth 2.0 / OIDC with short-lived JWT tokens signed by an identity broker.
3. **Authorization**: Implement Role-Based Access Control (RBAC) via IAM policies enforcing least privilege.
4. **Prevent Cyber Attacks**: Deploy AWS WAF and DDoS Protection (AWS Shield) at ingress gateways.
5. **Secure Communication**: Enforce mTLS (Mutual TLS) with X.509 certificates between edge devices and gateways.
6. **Ensure Availability**: Configure Auto-Scaling Groups and Multi-AZ Elastic Load Balancers (ELB).

---

## Task 12: IAM Table & Data-Protection Map

### IAM Role Table
| Role Name | Access Scope | Permissions |
| :--- | :--- | :--- |
| **Zone Operator** | Local Zone Subnet | Manage local job submission to *scheduler engine from Part 1* |
| **City Dashboard Admin** | VPC Central Scope | Full read/write access across all zone states and dashboards |
| **Auditor** | Global Read-Only | Read-only access to log archives and safety audit tables |

### Data Protection Matrix
* **At Rest**: AES-256 XTS encryption applied to `JOBS` metadata state stored on local disk partitions.
* **In Transit**: TLS 1.3 tunnel protecting public-safety alerts dispatched to the central dashboard.
* **In Use**: Process Isolation & Hardware Enclave Memory Protection securing the *Banker's Algorithm safety check running in memory*.

---

## Task 13: IoT Connectivity & Architecture Layers

### Devices & Communication Standards:
1. **Traffic Camera Trigger**: **5G** (High bandwidth, low latency required for video analysis).
2. **Environmental Sensor**: **LoRaWAN** (Long range, ultra-low power consumption for periodic updates).
3. **Wearable Public-Safety Device**: **NB-IoT** (Wide coverage, deep indoor penetration, low power).

### 6-Layer Mapping:
1. **Physical Environment**: Physical sensors deployed across urban sectors.
2. **Perception / Device Layer**: Hardware sensor modules and microcontroller interfaces.
3. **Gateway Layer**: Edge aggregation routers running mTLS protocol translation.
4. **Network Communication Layer**: Cellular 5G / LoRaWAN backhaul infrastructure.
5. **Cloud Platform Layer**: *The scheduler and Banker's Algorithm engine from Part 1*.
6. **Application Layer**: Smart City Operations management dashboard UI.

---

## Task 14: Threat Analysis & Mitigation
1. **Rogue Edge Node Injection**: An unauthorized node impersonates Zone-B.
   * *Mitigation*: Hardware TPM 2.0 device attestation coupled with mTLS X.509 client certificate validation.
2. **Denial of Service (DoS) on Ingress**: Flood of bogus sensor triggers targeting the job queue.
   * *Mitigation*: Rate-limiting at the Cloudflare/WAF edge coupled with Token Bucket throttling.
3. **Man-in-the-Middle (MitM) Tampering**: Interception of alert messages between Zone-A and Dashboard.
   * *Mitigation*: Mandatory TLS 1.3 with Certificate Pinning on edge client runtimes.
