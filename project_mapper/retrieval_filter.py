# retrieval_filter.py

import os



# =========================
# FILE PENALTIES
# =========================

PENALTY_FOLDERS = {

    "archive": 20,

    "__pycache__": 50,

    "history": 10,

    "outputs": 10,

    "snapshots": 15
}


PENALTY_FILES = {

    "old_": 25,

    "test_": 8
}



# =========================
# FILE BOOSTS
# =========================

BOOST_FOLDERS = {

    "attendance": 12,

    "accounts": 10,

    "leave_management": 10,

    "reports": 10,

    "templates": 5
}


BOOST_FILE_TYPES = {

    "django_view": 8,

    "django_model": 8,

    "django_url": 5
}



# =========================
# APPLY FILTERS
# =========================

def apply_retrieval_filters(results):

    filtered_results = []

    for result in results:

        chunk = result["chunk"]

        file_path = chunk.get(
            "file",
            ""
        ).lower()

        file_type = chunk.get(
            "type",
            ""
        ).lower()

        final_score = result.get(
            "score",
            0
        )


        # =========================
        # FOLDER PENALTIES
        # =========================

        for folder, penalty in PENALTY_FOLDERS.items():

            if folder in file_path:

                final_score -= penalty


        # =========================
        # FILE PENALTIES
        # =========================

        filename = os.path.basename(
            file_path
        )

        for keyword, penalty in PENALTY_FILES.items():

            if keyword in filename:

                final_score -= penalty


        # =========================
        # BOOST REAL APPS
        # =========================

        for folder, boost in BOOST_FOLDERS.items():

            if folder in file_path:

                final_score += boost


        # =========================
        # BOOST DJANGO FILE TYPES
        # =========================

        if file_type in BOOST_FILE_TYPES:

            final_score += BOOST_FILE_TYPES[
                file_type
            ]


        # SAVE UPDATED SCORE

        result["score"] = final_score

        result["final_score"] = final_score

        filtered_results.append(
            result
        )


    # SORT AGAIN

    filtered_results.sort(

        key=lambda x: x["score"],

        reverse=True
    )

    return filtered_results