function Projects() {
  return (
    <section>
      <h1>Projects</h1>
      <ul>
        <li>
          <strong>
            Kintsugi Protocol (KTN): Secure Satellite Data Transfer
          </strong>
          <p>
            Developed during the <em>ActInSpace</em> hackathon. A
            secure-by-design protocol concept tailored for the unique
            constraints of satellite communications.
          </p>
          <ul>
            <li>
              Designed a resilient security architecture to ensure data
              confidentiality and integrity in high-latency environments.
            </li>
            <li>
              Mitigated interception risks by implementing robust encryption and
              verification mechanisms.
            </li>
            <li>
              Researched protocol adaptability for space-grade,
              radiation-hardened hardware.
            </li>
            <li></li>
          </ul>
        </li>
        <li>
          <strong>
            Enterprise Zero Trust Access Architecture (HashiCorp Boundary)
          </strong>
          <p>
            Designed and documented a high-availability (HA) infrastructure for
            secure privileged access, integrating a complex ecosystem of
            security and monitoring tools.
          </p>
          <ul>
            <li>
              <strong>Identity & Access:</strong> Integrated
              <strong>Azure AD (OIDC/SCIM)</strong> for SSO and MFA,
              implementing
              <strong>Just-in-Time (JIT)</strong> credentials through
              <strong>HashiCorp Vault</strong> integration.
            </li>
            <li>
              <strong>Infrastructure as Code:</strong> Managed end-to-end
              deployment via
              <strong>GitLab CI/CD</strong>, using
              <strong>Terraform</strong> and
              <strong>Helm</strong> for automated environment provisioning.
            </li>
            <li>
              <strong>Security & Compliance:</strong> Designed a{" "}
              <strong>Defense-in-Depth</strong> network with
              <strong>DMZ, WAF</strong>, and micro-segmentation using
              <strong>Calico/Cilium</strong> Network Policies.
            </li>
            <li>
              <strong>Observability & Audit:</strong> Built a centralized
              logging and monitoring pipeline using{" "}
              <strong>Splunk (SIEM)</strong>,<strong>Prometheus</strong>, and
              <strong>Grafana</strong> for real-time security auditing.
            </li>
            <li>
              <strong>DevSecOps Pipeline:</strong> Automated security gates
              including
              <strong>SAST (tfsec)</strong>,<strong>SCA (Trivy)</strong>, and
              <strong>DAST (OWASP ZAP)</strong> to ensure supply chain security.
            </li>
            <li></li>
          </ul>
        </li>
        <li>
          <strong>
            Wishlist SaaS & Intelligent Data Extraction — In Progress
          </strong>
          <p>
            Developing a scalable gift-tracking platform featuring a resilient
            scraping engine and containerized backend infrastructure.
          </p>
          <ul>
            <li>
              <strong>Containerized Environment:</strong>
              Orchestrated the entire application stack using
              <strong>Docker</strong>, ensuring seamless deployment and
              environment isolation for backend services.
            </li>
            <li>
              <strong>Hybrid Parsing Engine:</strong>
              Engineered a two-tier data extraction system: a high-performance
              HTML parser for standard requests and an
              <strong>AI-driven fallback</strong> for complex, non-standard
              e-commerce structures.
            </li>
            <li>
              <strong>Proxy & Traffic Management:</strong>
              Integrated <strong>Mobile Proxies</strong> to tunnel full HTML
              page requests, bypassing anti-bot measures and ensuring 100% data
              retrieval reliability.
            </li>
            <li>
              <strong>Secure Networking:</strong> Established a private
              management layer via
              <strong>Tailscale</strong> for encrypted node-to-node connectivity
              and secure remote server administration.
            </li>
            <li>
              <strong>Automation Core:</strong> Leveraged
              <strong>n8n</strong> to synchronize Telegram Bot interactions with
              <strong>PostgreSQL</strong> and AI-based processing nodes.
            </li>
          </ul>
        </li>
      </ul>
    </section>
  );
}
export default Projects;
