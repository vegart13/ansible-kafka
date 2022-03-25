#!/usr/bin/python

from ast import Delete
from email.policy import default
from re import IGNORECASE
from unittest import result
from venv import create
from ansible.module_utils.basic import *
from ansible.module_utils.basic import AnsibleModule
import os
import subprocess



def main():

    # Set variables as global for cross-function accessability
    global module, create, delete, describe

    # Define available arguments/parameters a user can pass to the module
    # fields = {
        # "custom_bin_path":                              {"type": "str", "default": "kafka-topics"},
        # "create":                                       {"type": "bool", "default": False},
        # "delete":                                       {"type": "bool", "default": False},
        # "describe":                                     {"type": "bool", "default": False},
        # "topic_name":                                   {"required": True, "type": "str"},
        # "bootstrap_server":                             {"required": True, "type": "str"},
        # "port":                                         {"required": True, "type": "int"},
        # "command_config":                               {"type": "str"},
        # "cleanup_policy":                               {"type": "str"},
        # "confluent_key_schema_validation":              {"type": "str"},
        # "confluent_key_subject_name_strategy":          {"type": "str"},
        # "confluent_tier_enable":                        {"type": "str"},
        # "confluent_tier_local_hotset_bytes":            {"type": "str"},
        # "confluent_value_schema_validation":            {"type": "str"},
        # "confluent_value_subject_name_strategy":        {"type": "str"},
        # "delete_retention_ms":                          {"type": "str"},
        # "file_delete_ms":                               {"type": "str"},
        # "flush_ms":                                     {"type": "str"},
        # "follower_replication_throttled_replicas":      {"type": "str"},
        # "index_interval_bytes":                         {"type": "str"},
        # "leader_replication_throttled_replicas":        {"type": "str"},
        # "max_compaction_lag_ms":                        {"type": "str"},
        # "max_message_bytes":                            {"type": "str"},
        # "message_timestamp_type":                       {"type": "str"},
        # "min_cleanable_dirty_ratio":                    {"type": "str"},
        # "min_compaction_lag_ms":                        {"type": "str"},
        # "min_insync_replicas":                          {"type": "str"},
        # "preallocate":                                  {"type": "str"},
        # "retention_bytes":                              {"type": "str"},
        # "segment_bytes":                                {"type": "str"},
        # "segment_index_bytes":                          {"type": "str"},
        # "segment_jitter_ms":                            {"type": "str"},
        # "segment_ms":                                   {"type": "str"},
        # "unclean_leader_election_enable":               {"type": "str"},
        # "confluent_placement_constraints":              {"type": "str"},
        # "message_downconversion_enable":                {"type": "str"},
    # }

    module_args = dict(
        custom_bin_path=dict(type='str', default='kafka-topics'),
        create=dict(type='bool', default=False),
        delete=dict(type='bool', default=False),
        describe=dict(type='bool', default=False),
        topic_name=dict(type='str', required=True),
        port=dict(type='str', required=True)
    )

    # Store variables
    module = AnsibleModule(argument_spec=module_args)
    create = module.params['create']
    delete = module.params['delete']
    describe = module.params['describe']

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    
    validate_action_input()
    
    module.exit_json(changed=True, meta=module.params)

def validate_action_input():
    if create == True and delete == True and describe == False:
        module.fail_json(msg='Both create and delete cannot be True at the same time.')
    else: pass

    if create == True and describe == True and delete == False:
        module.fail_json(msg='Both create and describe cannot be True at the same time.')
    else: pass
    
    if delete == True and describe == True and create == False:
        module.fail_json(msg='Both describe and delete cannot be True at the same time.')
    else: pass

    if create == True and delete == True and describe == True:
        module.fail_json(msg='Create, describe and delete cannot be True at the same time.')
    else: pass

    if create == False and delete == False and describe == False:
        module.fail_json(msg='Create, describe or delete must be set True.')
    else: pass

    
    # validate_action_input()

# module.exit_json(changed=True, meta=module.params)

# def validate_action_input():
#     # Verify that only one action has been chosen
#     if str(create).lower == 'create' and str(delete).lower == str(delete).lower == 'delete':
#         module.fail_json(msg='Action must be set to Create, Describe or Delete')
#     else: module.fail_json(msg='Both create and delete cannot be True at the same time.')

# def create_action_string():
#     # Create string based on input
#     if str(create).lower == 'create':
#         module.params.update({"action": "~/Desktop/Kafka/bin/kafka-topics --create"})
#     elif str(delete).lower == 'delete':
#         module.params.update({"action": "~/Desktop/Kafka/bin/kafka-topics --delete"})
#     elif str(describe).lower == 'describe':
#         module.params.update({"action": "~/Desktop/Kafka/bin/kafka-topics --describe"})
#     else: module.fail_json(msg='Action must be set to Create, Describe or Delete')


# 3. Store string to variable and make accessible globally



    # match create:
    #     case True:
    #         action_string = kafka.params["custom_bin_path"] + " --create"
    #         return action_string
    #     case False:
    #         print("CREATE = FALSE")
    #         return action_string

    # match delete:
    #     case True:
    #         action_string = kafka.params["custom_bin_path"] + " --delete"
    #         return action_string
    #     case False:
    #         print("DELETE = FALSE")

    # match describe:
    #     case True:
    #         action_string = kafka.params["custom_bin_path"] + " --describe"
    #         return action_string
    #     case False:
    #         print("DESCRIBE = FALSE")



    ### REQUIRED PARAMETERS
    # Match action to Create, Describe or Delete and update command part. Error returned if mismatch.
    # if kafka.params["action"].lower() == "create":
    #     kafka.params.update({"action": "~/Desktop/Kafka/bin/kafka-topics --create"})
    # elif kafka.params["action"].lower() == "delete":
    #     kafka.params.update({"action": "~/Desktop/Kafka/bin/kafka-topics --delete "})
    # elif kafka.params["action"].lower() == "describe":
    #     kafka.params.update({"action": "~/Desktop/Kafka/bin/kafka-topics --describe"})
    # else: kafka.fail_json(msg='Action must be set to Create, Describe or Delete')

    ### SWITCH TEST


    # Add prefixes to command parameters (e.g.: --topic for topics, --bootstrap-server for bootstrap servers)
    # kafka.params.update({"bootstrap_server": "--bootstrap-server " + kafka.params["bootstrap_server"] + ":" + str(kafka.params["port"])})
    # kafka.params.update({"topic_name": "--topic " + kafka.params["topic_name"]})

    # ### OPTIONAL REQUIREMENTS
    # if kafka.params["command_config"] == '':
    #     pass    
    # else:
    #     kafka.params.update({"command_config": "COMMAND CONFIG NOT FOUND"})

    # if kafka.params["cleanup_policy"] == '':
    #     pass
    # else:
    #     kafka.params.update({"cleanup_policy": "--config " + "cleanup.policy=" + kafka.params["cleanup_policy"]})

    # Concatenate command based on updated variables
    # required_string = kafka.params["action"] + " " + \
    #                         kafka.params["bootstrap_server"] + " " + \
    #                         kafka.params["topic_name"]

    # Save command to param then convert to string
    # kafka.params.update({"test": required_string})
    # shellscript = str(kafka.params["test"])

    # Execute string on system
    #os.system(shellscript)

    # Exit
    #module.exit_json(changed=True, meta=module.params)
    # kafka.exit_json(changed=True, meta=kafka.params)

if __name__ == '__main__':
    main()
