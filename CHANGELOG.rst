Change Log
==========

0.3
---
-   Initial scaffolding and data model setup. This is a work in progress
    and is not yet ready for use.
-   The model for the Denig manuscript currently tracks pages, text, and images. 
    The current unit for a single page is a `Document`. A `Document` can contain
    multiple `Fragments`, here meaning single lines/sentences from the manuscript itself. 
    A number of `Fragments` can be associated with a `Document` to also allow for 
    translations.
-   The model also tracks translations (original German, modern German, and English)
    and the relationships between the translations. These are also tied to the 
    pages.