#!/usr/bin/env python3.11

import argparse
import random
import subprocess
import yaml
import os
import logging
import time

def setup_logging():
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    logging.basicConfig(filename=os.path.join(logs_dir, "ghostedme.log"), level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def get_persistent_volumes():
    try:
        # Get list of persistent volumes
        result = subprocess.run(['kubectl', 'get', 'pv', '--output', 'json'], capture_output=True, check=True)
        volumes = yaml.safe_load(result.stdout)

        return [volume['metadata']['name'] for volume in volumes['items']]
    except Exception as e:
        logging.error("Error retrieving persistent volumes:", exc_info=True)
        return []

def delete_persistent_volume(volume_name):
    try:
        # Delete persistent volume
        subprocess.run(['kubectl', 'delete', 'pv', volume_name], check=True)

        logging.info(f"Persistent volume '{volume_name}' deleted successfully")
        return True
    except Exception as e:
        logging.error(f"Error deleting persistent volume '{volume_name}':", exc_info=True)
        return False

def detach_persistent_volume(volume_name):
    try:
        # Detach persistent volume
        subprocess.run(['kubectl', 'patch', 'pv', volume_name, '-p', '{"spec":{"persistentVolumeReclaimPolicy":"Retain","claimRef":null}}'], check=True)

        logging.info(f"Persistent volume '{volume_name}' detached successfully")
        return True
    except Exception as e:
        logging.error(f"Error detaching persistent volume '{volume_name}':", exc_info=True)
        return False

def attach_persistent_volume(volume_name, claim_name, namespace):
    try:
        # Attach persistent volume
        subprocess.run(['kubectl', 'patch', 'pv', volume_name, '-p', f'{{"spec":{{"claimRef":{{"name":"{claim_name}","namespace":"{namespace}"}}}}}}'], check=True)

        logging.info(f"Persistent volume '{volume_name}' attached to claim '{claim_name}' in namespace '{namespace}' successfully")
        return True
    except Exception as e:
        logging.error(f"Error attaching persistent volume '{volume_name}' to claim '{claim_name}' in namespace '{namespace}':", exc_info=True)
        return False

def get_persistent_volume_claims():
    try:
        # Get list of persistent volume claims
        result = subprocess.run(['kubectl', 'get', 'pvc', '--all-namespaces', '--output', 'json'], capture_output=True, check=True)
        claims = yaml.safe_load(result.stdout)

        return [(claim['metadata']['name'], claim['metadata']['namespace']) for claim in claims['items']]
    except Exception as e:
        logging.error("Error retrieving persistent volume claims:", exc_info=True)
        return []

def delete_persistent_volume_claim(claim_name, namespace):
    try:
        # Delete persistent volume claim
        subprocess.run(['kubectl', 'delete', 'pvc', claim_name, '-n', namespace], check=True)

        logging.info(f"Persistent volume claim '{claim_name}' in namespace '{namespace}' deleted successfully")
        return True
    except Exception as e:
        logging.error(f"Error deleting persistent volume claim '{claim_name}' in namespace '{namespace}':", exc_info=True)
        return False

def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="GhostedMe - Randomly delete attached volumes and storage resources in a Kubernetes cluster")
    parser.add_argument("--timetoghost", type=int, help="Detached volume time in seconds")
    args = parser.parse_args()

    # Get list of persistent volumes
    volumes = get_persistent_volumes()

    if volumes:
        # Select a random persistent volume
        volume_to_delete = random.choice(volumes)

        # Detach the selected persistent volume if --timetoghost provided
        if args.timetoghost:
            if detach_persistent_volume(volume_to_delete):
                print(f"Detached volume '{volume_to_delete}', waiting {args.timetoghost} seconds...")
                time.sleep(args.timetoghost)
                print("Time's up! Reattaching volume...")
                # Reattach the persistent volume
                claims = get_persistent_volume_claims()
                if claims:
                    claim_to_attach, claim_namespace = random.choice(claims)
                    if attach_persistent_volume(volume_to_delete, claim_to_attach, claim_namespace):
                        print(f"Volume '{volume_to_delete}' reattached to claim '{claim_to_attach}' in namespace '{claim_namespace}' successfully")
                    else:
                        print(f"Failed to reattach volume '{volume_to_delete}'")
                else:
                    print("No persistent volume claims found")
            else:
                print(f"Failed to detach volume '{volume_to_delete}'")
        else:
            # Delete the selected persistent volume if --timetoghost not provided
            if delete_persistent_volume(volume_to_delete):
                # Delete associated persistent volume claim
                claims = get_persistent_volume_claims()
                if claims:
                    matching_claims = [(claim_name, namespace) for claim_name, namespace in claims if volume_to_delete in claim_name]
                    if matching_claims:
                        claim_to_delete, claim_namespace = random.choice(matching_claims)
                        if delete_persistent_volume_claim(claim_to_delete, claim_namespace):
                            print(f"Persistent volume '{volume_to_delete}' and claim '{claim_to_delete}' in namespace '{claim_namespace}' deleted successfully")
                        else:
                            print(f"Failed to delete persistent volume claim '{claim_to_delete}' in namespace '{claim_namespace}'")
                    else:
                        print(f"No matching persistent volume claims found for volume '{volume_to_delete}'")
                else:
                    print("No persistent volume claims found")
            else:
                print(f"Failed to delete volume '{volume_to_delete}'")
    else:
        print("No persistent volumes found")

if __name__ == "__main__":
    main()
