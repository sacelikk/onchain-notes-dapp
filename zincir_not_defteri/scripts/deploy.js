import { createWalletClient, createPublicClient, http } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { hardhat } from 'viem/chains';
import fs from 'fs';
import path from 'path';

async function main() {
  console.log('Sözleþme yerel aða yükleniyor...');

  const artifactPath = path.resolve('./artifacts/contracts/SecureNotes.sol/SecureNotes.json');
  const artifact = JSON.parse(fs.readFileSync(artifactPath, 'utf8'));

  // Account #0 private key
  const account = privateKeyToAccount('0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80');

  const client = createWalletClient({
    account,
    chain: hardhat,
    transport: http('http://127.0.0.1:8545')
  });

  const publicClient = createPublicClient({
    chain: hardhat,
    transport: http('http://127.0.0.1:8545')
  });

  const hash = await client.deployContract({
    abi: artifact.abi,
    bytecode: artifact.bytecode
  });

  console.log('Ýþlem onaylanýyor... Tx Hash:', hash);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });

  console.log('========================================');
  console.log('SecureNotes baþarýyla yüklendi!');
  console.log('Kontrat Adresi:', receipt.contractAddress);
  console.log('========================================');
}

main().catch((err) => {
  console.error('Hata:', err);
  process.exitCode = 1;
});
