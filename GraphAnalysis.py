"""
Analyze some graph data with lazy evaluation and streaming.

2015: Sang Han
"""

import os
import sys
import operator
import functools
import itertools
import boto

from os.path import join as jp

from configparser import ConfigParser

import graphlab as gl

def s3_signin(**auth):
    """
    Convenience function for validating keys  and providing
    access to bucket shares.
    
    Returns S3Object
    """
    home, cfg  = os.getenv('HOME'), ConfigParser()
    cred, user = jp(home, '.aws', 'credentials'), os.getlogin()
    token_ids = 'aws_access_key_id', 'aws_secret_access_key'
    
    cfg.read(cred)

    valid_user = user in cfg.sections()
    account    = itertools.repeat(user if valid_user else cfg.sections()[0], 2)

    # Authentication provided as function input overrides config file behavior
    valid_auth = all(auth.has_key(i) for i in token_ids)
    
    token      = zip(account, token_ids) if not valid_auth else [token_ids]
    store      = cfg if not auth else auth
    
    user_id    = dict(zip(token_ids, map(lambda t: store.get(*t), token)))
    
    if not all(user_id.values()):
        raise ValueError('No valid authorization found')

    return boto.connect_s3(**user_id)
    
