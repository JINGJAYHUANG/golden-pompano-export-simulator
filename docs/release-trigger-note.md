# Release trigger policy

A release is created only after the exact merged main commit passes the complete CI matrix. The immutable semantic-version tag must point to that verified commit; release assets are then rebuilt from the tag and revalidated.
