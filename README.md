# 🔐 Cloud-Cryptography-VPN-System
Implementation of a secure cloud and VPN-based cryptographic system for a simulated healthcare environment. The project demonstrates practical application of public key infrastructure, hybrid encryption techniques, and cryptographic protocols to secure sensitive medical data transmission and storage in a cloud-based distributed system.
## 📚 Academic Context
This project was developed as part of Unit 24: Applied Cryptography in the Cloud under the Pearson BTEC HND in Digital Technologies (Cyber Security). It demonstrates academic engagement with the unit requirements and assessment criteria for applied cryptographic systems in cloud environments.
## 📌 Project Overview
This project implements a secure cloud-based cryptographic system designed for a simulated healthcare environment (Al Shifa Hospital Network). The system secures sensitive healthcare data across distributed hospital branches connected to a central data hub using VPN-based communication and encryption techniques.
The implementation is based on three core datasets: Patient Administration Data (PAD), Patient Medical Data (PMD), and Patient Financial Data (PFD). Each dataset represents a different sensitivity level of healthcare information and is processed using appropriate cryptographic methods.

PAD and PFD are protected using AES-CBC block encryption to secure structured administrative and financial records, while PMD, which involves continuous medical monitoring data, is secured using ChaCha20 stream encryption for efficient real-time protection. All encryption keys are managed using RSA-based secure key wrapping, ensuring safe key exchange between systems.
The system integrates secure authentication through Public Key Infrastructure (PKI) and ensures data integrity through hashing mechanisms, providing a complete security layer for cloud-based healthcare data processing and transmission.
## 🧠 Key Features

- Implementation of a hybrid cryptographic system combining symmetric and asymmetric encryption techniques for secure cloud communication.  

- Use of AES-CBC block cipher to protect structured data such as Patient Administration Data (PAD) and Patient Finance Data (PFD).  

- Use of ChaCha20 stream cipher for efficient encryption of real-time Patient Medical Data (PMD) in a high-throughput environment.  

- Integration of RSA-based Public Key Infrastructure (PKI) for secure key exchange and authentication between distributed hospital nodes.  

- Secure VPN-based communication channel ensuring encrypted transmission between hospital branches and central data hub.  

- Hashing mechanism implemented to ensure data integrity and detect unauthorized modifications during storage and transmission.  

- Designed to support secure cloud migration by addressing scalability, confidentiality, and access control requirements in healthcare systems.  
## 🔐 PKI-Based Secure Communication Architecture
<p align="center">
  <img src="Images/PKI-Based Encryption and Decryption.png" width="850"/>
</p>
Encryption and decryption procedure: 

- The public key of the receiver is used to encrypt PAD/PMD/PFD.
  
- Ciphertext is transmitted on the ASHN VPN.
  
- Information is decrypted with the help of a private key to restore original data.
  
