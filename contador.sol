// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ContadorSimple {
    int256 private contador;
    address private owner;
    mapping(address => bool) private whitelist;

    // Eventos
    event ValorModificado(address indexed quien, int256 nuevoValor);

    // Modificadores
    modifier onlyOwner() {
        require(msg.sender == owner, "No eres el propietario del contrato");
        _;
    }

    modifier onlyWhitelisted() {
        require(whitelist[msg.sender], "No estas en la lista blanca");
        _;
    }

    // Constructor
    constructor() {
        owner = msg.sender;
        whitelist[owner] = true;  // el propietario inicialmente está en la lista blanca
    }

    // Funciones para administrar la whitelist
    function addToWhitelist(address _address) public onlyOwner {
        whitelist[_address] = true;
    }

    function removeFromWhitelist(address _address) public onlyOwner {
        whitelist[_address] = false;
    }

    function isWhitelisted(address _address) public view returns(bool) {
        return whitelist[_address];
    }

    // Funciones del contador
    function incrementar() public onlyWhitelisted {
        contador++;
        emit ValorModificado(msg.sender, contador);
    }

    function decrementar() public onlyWhitelisted {
        contador--;
        emit ValorModificado(msg.sender, contador);
    }

    function obtenerValor() public view onlyWhitelisted returns(int256) {
        return contador;
    }
}
