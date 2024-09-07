set(Namespace_SRCS
        freecad/cam_scripts/init_gui.py
        freecad/cam_scripts/__init__.py
        freecad/cam_scripts/my_numpy_function.py
        freecad/cam_scripts/translate_utils.py
        freecad/cam_scripts/version.py
        freecad/cam_scripts/resources/cool.svg
        freecad/cam_scripts/resources/translations/cam_scripts_es-ES.qm
        freecad/cam_scripts/resources/translations/cam_scripts_es-ES.ts
)

SOURCE_GROUP("" FILES ${Namespace_SRCS})

ADD_CUSTOM_TARGET(SEARCHBAR ALL
        SOURCES ${Namespace_SRCS}
)

fc_copy_sources(SEARCHBAR "${CMAKE_BINARY_DIR}/Mod/CamScripts" ${Namespace_SRCS})

INSTALL(
    FILES
        ${Namespace_SRCS}
    DESTINATION
        Mod/SearchBar
)
