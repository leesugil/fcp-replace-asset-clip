import xml.etree.ElementTree as ET

def parse_target(root, affix, debug=False):
    """
    Returns: [ { 'id': 'r2', 'name': 'affix_abc', 'target_name': 'abc', 'uid': 'xxx', 'start': '0s', 'duration': '405452/60s', 'hasVideo': '1', 'format': 'r3', 'hasAudio': '1', 'videoSources': '1', 'audioSources': '3', 'audioChannels': '2', 'audioRate': '48000' }, {}, ... ]
    """
    output = []
    resources = root.find('resources')
    for r in resources:
        if (r.tag == 'asset') and r.get('name').startswith(affix):
            data = {
                    'id': r.get('id'),
                    'name': r.get('name'),
                    'target_name': r.get('name').removeprefix(affix),
                    'uid': r.get('uid'),
                    'start': r.get('start'),
                    'duration': r.get('duration'),
                    'hasVideo': r.get('hasVideo'),
                    'format': r.get('format'),
                    'hasAudio': r.get('hasAudio'),
                    'videoSources': r.get('videoSources'),
                    'audioSources': r.get('audioSources'),
                    'audioChannels': r.get('audioChannels'),
                    'audioRate': r.get('audioRate')
                    }
            if debug:
                print(f"parse_target: parsed target info: {data}")
            output.append(data)
    return output

def replace_with_target(root, target, affix, debug=False):
    """
    target: [ { 'id': 'r2', 'name': 'affix_abc', 'target_name': 'abc', 'uid': 'xxx', 'start': '0s', 'duration': '405452/60s', 'hasVideo': '1', 'format': 'r3', 'hasAudio': '1', 'videoSources': '1', 'audioSources': '3', 'audioChannels': '2', 'audioRate': '48000' }, {}, ... ]
    """
    # replace all asset-clips, not only those in the main project timeline spine.
    asset_clips = root.findall('.//asset-clip')
    for c in asset_clips:
        for t in target:
            if c.get('name') == t.get('target_name'):
                if debug:
                    print(f"replace_with_target: found {c.get('name')} at {c.get('offset')} starting at {c.get('start')}")
                    print(f"{c.get('ref')} -> {t.get('id')}")
                    print(f"{c.get('name')} -> {t.get('name')}")
                    print(f"{c.get('format')} -> {t.get('format')}")
                c.set('ref', t.get('id'))
                c.set('name', t.get('name'))
                c.set('format', t.get('format'))
                for conform in c.findall('conform-rate'):
                    c.remove(conform)

    # some are not just clean asset-clips. this is a disaster.
    asset_clips = root.findall('.//asset-clip')
    resources = root.find('resources')
    for r in resources:
        if r.tag == 'media':
            for sequence in r.findall('sequence'):
                for spine in sequence.findall('spine'):
                    for c in spine:
                        for t in target:
                            if c.tag == 'clip' and (c.get('name') == t.get('target_name')):
                                if debug:
                                    print(f"replace_with_target: found {c.get('name')} at {c.get('offset')} starting at {c.get('start')}")
                                    print(f"{c.get('name')} -> {t.get('name')}")
                                    print(f"{c.get('format')} -> {t.get('format')}")
                                c.set('name', t.get('name'))
                                c.set('format', t.get('format'))
                                for conform in c.findall('conform-rate'):
                                    c.remove(conform)
                                for video in c.findall('video'):
                                    if debug:
                                        # check if this is the right substitution
                                        print(f"{video.get('ref')} -> {t.get('id')}")
                                    video.set('ref', t.get('id'))
                                    for audio in video.findall('audio'):
                                        if debug:
                                            # check if this is the right substitution
                                            print(f"{audio.get('ref')} -> {t.get('id')}")
                                        audio.set('ref', t.get('id'))

